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
from settings import TARGET_ENCODING

URL = 'http://excf.com/bbs/write.php'
URL_POST = 'http://excf.com/bbs/write_ok.php'

def handle_get(request, path):
    redir = redirect_if_no_session(request)
    if redir:
        return redir

    args = path.split('/')

    if len(args) < 2:
        return error(request, u'잘못된 인자입니다.')

    dest = args[0]
    no = int(args[1])

    query = URL + '?id=%s&no=%d&mode=modify' % (pagedefs.PAGE_IDS[dest], no)
        
    result = remote.send_request(request, query, referer=URL)
    html, soup = remote.postprocess(result.read())
        
    redir = redirect_if_not_signed_on(request, html, soup, pagedefs.PAGE_PARSERS[dest])
    if redir:
        return redir

    errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(html, soup)
    if errcode != parser.ERROR_NONE:
        return error_forward(request, errmsg)
    
    data = default_template_vars(u'%s - 글 수정' % pagedefs.PAGE_NAMES[dest], request, dest)
    
    data.update(pagedefs.PAGE_PARSERS[dest].check_write(dest, html, soup))
    
    data['bid'] = dest
    data['target'] = '/modify/%s/%d' % (dest, no)
    
    return render_to_response('post.html', data)

def handle_post(request, path):
    redir = redirect_if_no_session(request)
    if redir:
        return
    
    args = path.split('/')

    if len(args) < 2:
        return error(request, u'잘못된 인자입니다.')

    dest = args[0]
    no = int(args[1])

    try:
        subject = request.POST['subject'].encode(TARGET_ENCODING)
        contents = request.POST['contents'].encode(TARGET_ENCODING)

        if not subject or not contents:
            raise Exception
    except:
        return error(request, u'내용을 입력해 주셔야 합니다.')
    
    query = {'subject': subject, 'memo': contents, 'mode': 'modify', 'id': pagedefs.PAGE_IDS[dest], 'use_html': '1', 'no': no}

    try:
        query['category'] = request.POST['category']
    except:
        pass
    
    l = remote.send_request(request, URL_POST, urllib.urlencode(query), referer=URL_POST)
    result, soup = remote.postprocess(l.read())

    errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(result, soup)
    if errcode != parser.ERROR_NONE:
        return error_forward(request, errmsg)

    return redirect('/view/%s/%d' % (dest, no))

def handle(request, path):
    if request.method == 'GET':
        return handle_get(request, path)
    else:
        return handle_post(request, path)
