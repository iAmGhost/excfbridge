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
from flexigate.tools import *

URL = 'http://excf.com/bbs/zboard.php'

def handle(request, path):
    try:
        redirect_if_no_session(request)

        args = path.split('/')

        dest = args[0]
        page = 1

        if len(args) > 1:
            page = int(args[1])

        if not pagedefs.PAGE_IDS.has_key(dest):
            return error(request, u'정의되지 않은 페이지입니다.')
        
        query = URL + '?id=%s&page=%d' % (pagedefs.PAGE_IDS[dest], page)

        result = remote.send_request(request, query)
        html, soup = remote.postprocess(result.read())

        redirect_if_not_signed_on(request, html, soup, pagedefs.PAGE_PARSERS[dest])
        
        errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(request, html, soup)
        if errcode:
            return error_forward(request, errmsg)

        output = pagedefs.PAGE_PARSERS[dest].parse_list(dest, html, soup)
        output['bid'] = dest
        output['page'] = page

        maxpages = 500 # FIXME
        pages = filter(lambda x: x > 0 and x <= maxpages, range(page-2, page+3))
        output['pages'] = pages

        data = default_template_vars(u'%s - %d 페이지' % (pagedefs.PAGE_NAMES[dest], page), request, dest)
        data.update(output)

        return render_to_response('list.html', data)
    except redirection, e:
        return e.where
