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
from settings import TARGET_SITE

URL_DELETE_POST = TARGET_SITE + '/delete_ok.php'
URL_DELETE_COMMENT = TARGET_SITE + '/del_comment_ok.php'

def handle_delete_post(request, path):
    try:
        redirect_if_no_session(request)
    
        args = path.split('/')

        if len(args) < 2:
            return error(request, u'잘못된 인자입니다.')

        dest = args[0]
        no = int(args[1])

        query = {'id': pagedefs.PAGE_IDS[dest], 'no': no}

        l = remote.send_request(request, URL_DELETE_POST, urllib.urlencode(query), referer=URL_DELETE_POST)
        result, soup = remote.postprocess(l.read())

        redirect_if_not_signed_on(request, result, soup, pagedefs.PAGE_PARSERS[dest])

        errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(request, result, soup)
        if errcode:
            return error_forward(request, errmsg)
    except redirection, e:
        return e.where

    return redirect('/list/%s' % dest)

def handle_delete_comment(request, path):
    try:
        redirect_if_no_session(request)
        
        args = path.split('/')

        if len(args) < 3:
            return error(request, u'잘못된 인자입니다.')

        dest = args[0]
        no = int(args[1])
        cno = int(args[2])

        query = {'id': pagedefs.PAGE_IDS[dest], 'no': no, 'c_no': cno}

        l = remote.send_request(request, URL_DELETE_COMMENT, urllib.urlencode(query), referer=URL_DELETE_COMMENT)
        result, soup = remote.postprocess(l.read())

        redirect_if_not_signed_on(request, result, soup, pagedefs.PAGE_PARSERS[dest])

        errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(request, result, soup)
        if errcode:
            return error_forward(request, errmsg)
    except redirection, e:
        return e.where

    return redirect('/view/%s/%d' % (dest, no))
