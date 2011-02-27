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

from page import page
import pagedefs
from parser import parser
import remote

class post(page):
    """ post handler """

    URL = 'http://excf.com/bbs/write_ok.php'
    URL_WRITE = 'http://excf.com/bbs/write.php'

    def check_arg(self, path):
        args = path.split('/')

        if len(args) < 1:
            self.error(u'게시판을 선택해야 합니다.')
            return None

        dest = args[0]
        
        if not pagedefs.PAGE_IDS.has_key(dest):
            self.error(u'정의되지 않은 페이지입니다.')
            return None

        return dest

    def post(self, path):
        if self.redirect_if_no_session():
            return

        dest = self.check_arg(path)
        if not dest:
            return

        subject = self.request.get('subject').encode('cp949')
        contents = self.request.get('contents').encode('cp949')
        
        query = {'subject': subject, 'memo': contents, 'mode': 'write', 'id': pagedefs.PAGE_IDS[dest], 'use_html': '1'}

        l = remote.send_request(self, self.URL, urllib.urlencode(query), referer=self.URL)
        result, soup = remote.postprocess(l.read())

        errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(result, soup)
        if errcode != parser.ERROR_NONE:
            self.error_forward(errmsg)
            return

        self.redirect('/list/%s' % (dest, ))

    def get(self, path):
        if self.redirect_if_no_session():
            return

        dest = self.check_arg(path)
        if not dest:
            return

        query = self.URL_WRITE + '?id=%s' % (pagedefs.PAGE_IDS[dest])
        
        result = remote.send_request(self, query, referer=self.URL_WRITE)
        html, soup = remote.postprocess(result.read())
        
        if self.redirect_if_not_signed_on(html, soup, pagedefs.PAGE_PARSERS[dest]):
            return

        errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(html, soup)
        if errcode != parser.ERROR_NONE:
            self.error_forward(errmsg)
            return

        self.set_title(u'%s - 새 글 쓰기' % pagedefs.PAGE_NAMES[dest])
        self.render('post.html.frag', {'bid': dest})

class post_comment(page):
    """ comment post handler """
    
    URL = 'http://excf.com/bbs/comment_ok.php'
    URL_REFERER = 'http://excf.com/bbs/view.php'

    def post(self, path):
        if self.redirect_if_no_session():
            return

        args = path.split('/')

        if len(args) < 2:
            self.error(u'잘못된 인자입니다.')
            return
        
        dest = args[0]
        no = args[1]

        if not pagedefs.PAGE_IDS.has_key(dest):
            self.error(u'정의되지 않은 페이지입니다.')
            return

        memo = self.request.get('comment').encode('cp949')

        query = {'id': pagedefs.PAGE_IDS[dest], 'no': no, 'memo': memo}

        l = remote.send_request(self, self.URL, urllib.urlencode(query), referer=self.URL_REFERER)
        result, soup = remote.postprocess(l.read())

        errcode, errmsg = pagedefs.PAGE_PARSERS[dest].check_error(result, soup)
        if errcode != parser.ERROR_NONE:
            self.error_forward(errmsg)
            return

        self.redirect('/view/%s/%s' % (dest, no))
