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

import re
from BeautifulSoup import BeautifulSoup

class parser:
    def parse_list(self, page):
        return

    def parse_view(self, page):
        return

    def check_session(self, page):
        return

class parser_free(parser):
    def parse_list(self, page):
        output = {}
        alist = []
        output['article_lists'] = alist
        
        soup = BeautifulSoup(page)
        trs = soup.findAll('tr')[3:]

        for tags in trs:
            if '<a href="view.php?' in str(tags):
                title = tags.contents[7].getText().replace('&nbsp;', ' ').replace('/span>', '').strip()
                author = tags.contents[9].getText().replace('/span>', '').strip()

                try:
                    title = title[title.rindex('>')+1:]
                except:
                    pass

                alist.append({'name': title, 'author': author})
        
        return output

    def check_session(self, page):
        if u"""<td align='center'>사용권한이 없습니다</td>""" in page:
            return False
        
        return True

