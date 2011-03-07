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

import os
import urllib

from flexigate.parser import parser
from flexigate import pagedefs, remote
from flexigate.tools import *
from settings import UPLOAD_PATH, UPLOAD_URL

URL_POST = 'http://excf.com/bbs/write_ok.php'
URL_POST_COMMENT = 'http://excf.com/bbs/comment_ok.php'
URL_POST_PAGE = 'http://excf.com/bbs/write.php'
URL_REFERER = 'http://excf.com/bbs/view.php'

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
    redir = redirect_if_no_session(request)
    if redir:
        return redir
    
    sid = get_session_id(request)

    dest = check_arg(path)
    if not dest:
        return error(request, u'잘못된 인자입니다.')

    try:
        subject = request.POST['subject'].encode('cp949')
        contents = request.POST['contents'].encode('cp949')

        if not subject or not contents:
            raise Exception
    except:
        return error(request, u'내용을 입력해 주셔야 합니다.')

    if request.FILES.has_key('file'):
        retrycnt = 0
        while True:
            if retrycnt == 0:
                filename = '%s_%s' % (sid, request.FILES['file'].name)
            else:
                filename = '%s_%d_%s' % (sid, retrycnt, request.FILES['file'].name)
            fpath = '%s/%s' % (UPLOAD_PATH, filename)

            if not os.path.exists(fpath):
                break
            retrycnt += 1 
     
        f = open(fpath, 'wb+')
        for chunk in request.FILES['file'].chunks():
            f.write(chunk)
        f.close()

        cx = '<img src=\'%s/%s\' alt=\'%s\' />\n\n' % (UPLOAD_URL, filename, request.FILES['file'].name)
        contents = cx.encode('cp949') + contents
    
    query = {'subject': subject, 'memo': contents, 'mode': 'write', 'id': pagedefs.PAGE_IDS[dest], 'use_html': '1'}

    try:
        query['category'] = request.POST['category']
    except:
        pass
    
    l = remote.send_request(request, URL_POST, urllib.urlencode(query), referer=URL_REFERER)
    result, soup = remote.postprocess(l.read())

    errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(result, soup)
    if errcode != parser.ERROR_NONE:
        return error_forward(request, errmsg)

    return redirect('/list/%s' % dest)

# GET handler
def handle_article_get(request, path):
    redir = redirect_if_no_session(request)
    if redir:
        return redir

    dest = check_arg(path)
    if not dest:
        return error(request, u'잘못된 인자입니다.')

    query = URL_POST_PAGE + '?id=%s' % (pagedefs.PAGE_IDS[dest])
        
    result = remote.send_request(request, query, referer=URL_POST_PAGE)
    html, soup = remote.postprocess(result.read())
        
    redir = redirect_if_not_signed_on(request, html, soup, pagedefs.PAGE_PARSERS[dest])
    if redir:
        return redir

    errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(html, soup)
    if errcode != parser.ERROR_NONE:
        return error_forward(request, errmsg)
    
    data = default_template_vars(u'%s - 새 글 쓰기' % pagedefs.PAGE_NAMES[dest], request, dest)
    
    data.update(pagedefs.PAGE_PARSERS[dest].check_write(dest, html, soup))
    
    data['bid'] = dest
    data['target'] = '/post/%s' % dest
    data['mode'] = 'post'
    
    return render_to_response('post.html', data)

# Handler for posting article
def handle_article(request, path):
    if request.method == 'GET':
        return handle_article_get(request, path)
    else:
        return handle_article_post(request, path)

# Handler for posting comment
def handle_comment(request, path):
    redir = redirect_if_no_session(request)
    if redir:
        return redir
    
    args = path.split('/')
    if len(args) < 2:
        return error(request, u'잘못된 인자입니다.')
        
    dest = args[0]
    no = args[1]

    if not pagedefs.PAGE_IDS.has_key(dest):
        return error(request, u'정의되지 않은 페이지입니다.')

    try:
        memo = request.POST['comment'].encode('cp949')
    except:
        return error(request, u'내용을 입력하셔야 합니다.')

    query = {'id': pagedefs.PAGE_IDS[dest], 'no': no, 'memo': memo}

    l = remote.send_request(request, URL_POST_COMMENT, urllib.urlencode(query), referer=URL_REFERER)
    result, soup = remote.postprocess(l.read())

    errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(result, soup)
    if errcode != parser.ERROR_NONE:
        return error_forward(request, errmsg)
    
    return redirect('/view/%s/%s' % (dest, no))
