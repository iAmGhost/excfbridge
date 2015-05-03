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

from django.http import HttpResponse
import urllib
from md5 import md5

from flexigate.parser import parser
from flexigate.parsers.common import get_zantan
from flexigate import pagedefs, remote, uploader, registry
from flexigate.tools import *
from settings import TARGET_ENCODING, TARGET_SITE

import random

URL_POST = TARGET_SITE + '/write_ok.php'
URL_POST_COMMENT = TARGET_SITE + '/comment_ok.php'
URL_POST_PAGE = TARGET_SITE + '/write.php'
URL_REFERER = TARGET_SITE + '/view.php'

def manuzelizer(data):
    out = []
    for i in data.split(u'\n'):
        trailing = u''
        i = i.strip()

        if not i:
            out.append(u'')
            continue

        for j in i[::-1]:
            if j == '.' or j == '!' or j == '?' or j == ';' or j == ' ' or j == u'ㅋ' or j == u'ㅎ':
                trailing += j
            else:
                break

        trailing = trailing[::-1]
        if len(trailing) > 0:
            stmp = i[:-len(trailing)]
        else:
            stmp = i

        if random.choice(range(3)) != 0:
            if stmp.endswith(u'요') or stmp.endswith(u'오'):
                stmp += u'동' * random.choice(range(1, 7)) + u'도' * random.choice(range(1, 4)) + u'동'
            elif stmp.endswith(u'다'):
                stmp += u'당' * random.choice(range(1, 7)) + u'다' * random.choice(range(1, 4)) + u'당'
            elif stmp.endswith(u'데'):
                stmp += u'뎅' * random.choice(range(1, 6)) + u'딍'
            else:
                stmp += u'디기딩' * random.choice(range(5))

        out.append(stmp + trailing)

    return u'\n'.join(out)

def check_arg(path):
    args = path.split('/')

    if len(args) < 1:
        return None

    dest = args[0]
        
    if not pagedefs.PAGE_IDS.has_key(dest):
        return None

    return dest

# POST handler
def handle_article_post(request, path):
    try:
        redirect_if_no_session(request)
        sid = get_session_id(request)
        sess = registry.query(sid)
        
        dest = check_arg(path)
        if not dest:
            return error(request, u'잘못된 인자입니다.')

        try:
            subject = request.POST['subject'].encode(TARGET_ENCODING)
            contents = request.POST['contents'].encode(TARGET_ENCODING)
        
            if not subject or not contents:
                raise Exception
        except:
            return error(request, u'내용을 입력해 주셔야 합니다.')

	keys = map(lambda x: 'file%d' % x, sorted(map(lambda x: int(x[4:]), request.FILES.keys())))
        keys.reverse()
        for f in keys:
            try:
                prefs = registry.get_prefs(sid)
                url = uploader.upload(request, request.FILES[f], size=prefs.photo_resize, bid=dest, uid=sess[0])
                cx = '<img src=\'%s\' alt=\'%s\' />\n\n' % (url, request.FILES[f].name)
            except Exception, e:
                cx = u'업로드 실패하였습니다: <b>%s</b> (%s)\n\n' % (request.FILES[f].name, str(e))
                
            contents = cx.encode(TARGET_ENCODING) + contents
    
        query = {'subject': subject, 'memo': contents, 'mode': 'write', 'id': pagedefs.PAGE_IDS[dest], 'use_html': '1'}

        try:
            query['category'] = request.POST['category']
        except:
            pass

        l = remote.send_request(request, URL_POST, urllib.urlencode(query), referer=URL_REFERER)
        result, soup = remote.postprocess(l.read())

        redirect_if_not_signed_on(request, result, soup, pagedefs.PAGE_PARSERS[dest])

        errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(request, result, soup)
        if errcode:
            return error_forward(request, errmsg)
    except redirection, e:
        return e.where

    response = redirect('/list/%s' % dest)
    response.delete_cookie('unsaved_body')
    response.delete_cookie('unsaved_subject')

    return response

# GET handler
def handle_article_get(request, path):
    try:
        redirect_if_no_session(request)

        sid = get_session_id(request)
        sess = registry.query(sid)
        prefs = registry.get_prefs(sid)

        dest = check_arg(path)
        if not dest:
            return error(request, u'잘못된 인자입니다.')

        query = URL_POST_PAGE + '?id=%s' % (pagedefs.PAGE_IDS[dest])
        
        result = remote.send_request(request, query, referer=URL_POST_PAGE)
        html, soup = remote.postprocess(result.read())
        
        redirect_if_not_signed_on(request, html, soup, pagedefs.PAGE_PARSERS[dest])

        errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(request, html, soup)
        if errcode:
            return error_forward(request, errmsg)
    
        data = default_template_vars(u'%s - 새 글 쓰기' % pagedefs.PAGE_NAMES[dest], request, dest)
    
        data.update(pagedefs.PAGE_PARSERS[dest].check_write(dest, html, soup))

        if request.META['HTTP_USER_AGENT']:
            ua = request.META['HTTP_USER_AGENT']
            if (('iPhone' in ua or 'iPod' in ua) and 'iPhone OS' in ua) or 'iPad' in ua:
                if 'OS 6_' in ua or 'OS 7_' in ua or 'OS 8_' in ua:
                    pass
                else:
                    data['iphone'] = True
                    data['session'] = md5(request.COOKIES['session']).hexdigest()

        if dest == 'free':
            zantan = 15 - get_zantan(request)
            if zantan:
                data['zantan'] = zantan

        if prefs.photo_resize:
            data['size'] = prefs.photo_resize
    
        data['bid'] = dest
        data['target'] = '/post/%s' % dest
        data['mode'] = 'post'
    except redirection, e:
        return e.where
    
    return render_to_response('post.html', data)

import traceback

# Handler for picup uploader
def handle_picup(request, path):
    if not request.FILES.has_key('filedata') and not request.POST.has_key('sid'):
        return HttpResponse('no image', mimetype='text/plain')

    try:
        url = uploader.upload(request, request.FILES['filedata'], size=0, sid=request.POST['sid'])
    except Exception, e:
        return HttpResponse(repr(e), mimetype='text/plain')

    return HttpResponse(url, mimetype='text/plain')

# Handler for posting article
def handle_article(request, path):
    if request.method == 'GET':
        return handle_article_get(request, path)
    else:
        return handle_article_post(request, path)

# Handler for posting comment
def handle_comment(request, path):
    try:
        redirect_if_no_session(request)
        
        args = path.split('/')
        if len(args) < 2:
            return error(request, u'잘못된 인자입니다.')
        
        dest = args[0]
        no = args[1]

        if not pagedefs.PAGE_IDS.has_key(dest):
            return error(request, u'정의되지 않은 페이지입니다.')

        try:
            memo = request.POST['comment'].encode(TARGET_ENCODING)
        except:
            return error(request, u'내용을 입력하셔야 합니다.')

        query = {'id': pagedefs.PAGE_IDS[dest], 'no': no, 'memo': memo}

        l = remote.send_request(request, URL_POST_COMMENT, urllib.urlencode(query), referer=URL_REFERER)
        result, soup = remote.postprocess(l.read())

        redirect_if_not_signed_on(request, result, soup, pagedefs.PAGE_PARSERS[dest])

        errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(request, result, soup)
        if errcode:
            return error_forward(request, errmsg)
    except redirection, e:
        return e.where
    
    return redirect('/view/%s/%s' % (dest, no))
