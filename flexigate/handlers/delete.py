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

URL_DELETE_POST = 'http://excf.com/bbs/delete_ok.php'
URL_DELETE_COMMENT = 'http://excf.com/bbs/del_comment_ok.php'

def handle_delete_post(request, path):
    redir = redirect_if_no_session(request)
    if redir:
        return
    
    args = path.split('/')

    if len(args) < 2:
        return error(request, u'잘못된 인자입니다.')

    dest = args[0]
    no = int(args[1])

    query = {'id': pagedefs.PAGE_IDS[dest], 'no': no}

    l = remote.send_request(request, URL_DELETE_POST, urllib.urlencode(query), referer=URL_DELETE_POST)
    result, soup = remote.postprocess(l.read())

    errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(result, soup)
    if errcode:
        return error_forward(request, errmsg)

    return redirect('/list/%s' % dest)

def handle_delete_comment(request, path):
    redir = redirect_if_no_session(request)
    if redir:
        return
    
    args = path.split('/')

    if len(args) < 3:
        return error(request, u'잘못된 인자입니다.')

    dest = args[0]
    no = int(args[1])
    cno = int(args[2])

    query = {'id': pagedefs.PAGE_IDS[dest], 'no': no, 'c_no': cno}

    l = remote.send_request(request, URL_DELETE_COMMENT, urllib.urlencode(query), referer=URL_DELETE_COMMENT)
    result, soup = remote.postprocess(l.read())

    errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(result, soup)
    if errcode:
        return error_forward(request, errmsg)

    return redirect('/view/%s/%d' % (dest, no))
