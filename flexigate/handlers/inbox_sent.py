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
from flexigate.parsers import common, inbox_sent
from flexigate.tools import *
from settings import TARGET_ENCODING, TARGET_SITE

URL = TARGET_SITE + '/member_memo2.php'

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

        data = default_template_vars(u'보낸 쪽지함 - %d 페이지' % (page), request, 'inbox_sent')
        data.update(inbox_sent.parse_list(html, soup))
        data['pages'] = filter(lambda x: x > 0 and x <= data['maxpages'], range(page-2, page+3))
        data['page'] = page

        return render_to_response('inbox_sent_list.html', data)
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

        output = inbox_sent.parse_view(html, soup)

        data = default_template_vars(u'보낸 쪽지함 - %s' % (output['topic']), request, 'inbox_sent')
        data.update(output)
        data['no'] = no

        return render_to_response('inbox_sent_view.html', data)
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
        
        return redirect('/inbox_sent')
    except redirection, e:
        return e.where
