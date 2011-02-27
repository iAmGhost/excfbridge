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

from page import page
import pagedefs
from parser import parser
import remote

class view(page):
    """ hander for post body view """

    URL = 'http://excf.com/bbs/view.php'

    def get(self, path):
        if self.redirect_if_no_session():
            return

        args = path.split('/')

        if len(args) < 2:
            self.error(u'잘못된 인자입니다.')
            return

        dest = args[0]
        no = int(args[1])

        if not pagedefs.PAGE_IDS.has_key(dest):
            self.error(u'정의되지 않은 페이지입니다.')
            return

        query = self.URL + "?id=%s&no=%d" % (pagedefs.PAGE_IDS[dest], no)

        result = remote.send_request(self, query)
        html, soup = remote.postprocess(result.read())

        if self.redirect_if_not_signed_on(html, soup, pagedefs.PAGE_PARSERS[dest]):
            return

        errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(html, soup)
        if errcode != parser.ERROR_NONE:
            self.error_forward(errmsg)
            return

        output = pagedefs.PAGE_PARSERS[dest].parse_view(dest, html, soup)
        output['bid'] = dest
        output['pid'] = no

        self.set_title(u'%s - %s' % (pagedefs.PAGE_NAMES[dest], output['subject']))
        self.render('view.html.frag', output)
