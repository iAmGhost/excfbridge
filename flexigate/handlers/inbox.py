# -*- coding: utf-8; -*-

# ExCF mobile gateway
# converts ExCF(http://excf.com) website to mobile-friendly manner.
#
# Copyright (c) 2011 Park "segfault" Joon-Kyu <mastermind@planetmono.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from django.shortcuts import render_to_response

from flexigate import remote, pagedefs
from flexigate.parser import parser
from flexigate.parsers import common, inbox
from flexigate.tools import *
from settings import TARGET_ENCODING

URL = 'http://excf.com/bbs/member_memo.php'
URL_NEW_MEMO = 'http://excf.com/bbs/view_info.php'
URL_SEND_MEMO = 'http://excf.com/bbs/send_message.php'
URL_REFERER = URL_NEW_MEMO

def redirect_if_not_signed_on(request, page, soup):
    print type(page)
    if u'alert("로그인된 회원만이 사용할수 있습니다");' in page:
        # Remote session is expired
        redir = redirect('/signon?%s' % urllib.urlencode({'redirect': request.path})) 
        force_sign_out(request, redir)
        raise redirection(redir)

def handle_list(request, path):
    try:
        redirect_if_no_session(request)

        args = path.split('/')

        try:
            page = int(args[0])
        except:
            page = 1

        query = URL + '?page=%d' % page
        result = remote.send_request(request, query)
        html, soup = remote.postprocess(result.read())

        redirect_if_not_signed_on(request, html, soup)

        data = default_template_vars(u'받은 쪽지함 - %d 페이지' % (page), request, 'inbox')
        data.update(inbox.parse_list(html, soup))
        data['pages'] = filter(lambda x: x > 0 and x <= data['maxpages'], range(page-2, page+3))
        data['page'] = page

        return render_to_response('inbox_list.html', data)
    except redirection, e:
        return e.where

def handle_view(request, path):
    try:
        redirect_if_no_session(request)

        try:
            args = path.split('/')
            no = int(args[0])
        except:
            return error(request, u'잘못된 요청입니다.')

        query = URL + '?exec=view&no=%d' % no
        result = remote.send_request(request, query)
        html, soup = remote.postprocess(result.read())

        redirect_if_not_signed_on(request, html, soup)

        output = inbox.parse_view(html, soup)

        data = default_template_vars(u'받은 쪽지함 - %s' % (output['topic']), request, 'inbox')
        data.update(output)
        data['no'] = no

        return render_to_response('inbox_view.html', data)
    except redirection, e:
        return e.where

def handle_send_get(request, uid):
    query = URL_NEW_MEMO + '?member_no=%d' % uid
    result = remote.send_request(request, query)
    html, soup = remote.postprocess(result.read())

    redirect_if_not_signed_on(request, html, soup)

    data = default_template_vars(u'새 쪽지', request)
    try:
        data.update(inbox.parse_new(html, soup))
    except:
        return error(request, u'없는 사용자입니다.')
    data['uid'] = uid
    if request.GET.has_key('qp'):
        data['redirect_to'] = request.GET['qp']

    return render_to_response('inbox_new.html', data)

def handle_send_post(request, uid):
    if request.GET.has_key('qp'):
        redir = request.GET['qp']
    else:
        redir = '/inbox'
    
    try:
        topic = request.POST['subject'].encode(TARGET_ENCODING)
        body = request.POST['body'].encode(TARGET_ENCODING)
    except:
        return error(u'내용을 입력해 주십시오.')

    query = {'html': '1', 'member_no': str(uid), 'kind': '1', 'subject': topic, 'memo': body}
    l = remote.send_request(request, URL_SEND_MEMO, urllib.urlencode(query), referer=URL_REFERER)
    result, soup = remote.postprocess(l.read())

    redirect_if_not_signed_on(request, result, soup)

    response = redirect(redir)
    response.delete_cookie('unsaved_body')
    response.delete_cookie('unsaved_subject')

    return response

def handle_send(request, path):
    try:
        redirect_if_no_session(request)

        try:
            args = path.split('/')
            uid = int(args[0])
        except:
            return error(request, u'잘못된 요청입니다.')

        if request.method == 'GET':
            return handle_send_get(request, uid)
        else:
            return handle_send_post(request, uid)
    except redirection, e:
        return e.where

def handle_delete(request, path):
    try:
        redirect_if_no_session(request)

        try:
            args = path.split('/')
            no = int(args[0])
        except:
            return error

        query = URL + '?exec=del&no=%d' % no
        result = remote.send_request(request, query)
        html, soup = remote.postprocess(result.read())

        redirect_if_not_signed_on(request, html, soup)
        
        return redirect('/inbox')
    except redirection, e:
        return e.where
