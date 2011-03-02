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

import urllib

from flexigate.parser import parser
from flexigate import pagedefs, remote
from flexigate.tools import *

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
        return
    
    dest = check_arg(path)
    if not dest:
        return error(request, u'잘못된 인자입니다.')

    try:
        subject = request.POST['subject'].encode('cp949')
        contents = request.POST['contents'].encode('cp949')
    except:
        return error(request, u'내용을 입력해 주셔야 합니다.')
    
    query = {'subject': subject, 'memo': contents, 'mode': 'write', 'id': pagedefs.PAGE_IDS[dest], 'use_html': '1'}
    
    l = remote.send_request(request, URL_POST, urllib.urlencode(query), referer=URL_REFERER)
    result, soup = remote.postprocess(l.read())

    errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(result, soup)
    if errcode != parser.ERROR_NONE:
        return error_forward(errmsg)

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
        return error_forward(errmsg)
    
    data = default_template_vars(u'%s - 새 글 쓰기' % pagedefs.PAGE_NAMES[dest], request)
    data['bid'] = dest
    
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
