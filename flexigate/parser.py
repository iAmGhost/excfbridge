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

# BeautifulSoup's HTML parsing capability is somewhat problematic, so
# we have to do additional (dirty) shovelling to get the desired result.

import re

def postprocess_string(text):
    return text.replace('&nbsp;', ' ').strip().replace('/span>', '')

find_attr = lambda node, attr: filter(lambda x: x[0] == attr, node.attrs)[0][1]

class parser:
    ERROR_SIGNED_OUT = 1
    ERROR_THROTTLE_LIMIT = 2
    ERROR_GENERIC = 3

    no_matcher = re.compile(r'.*no=(\d+)')
    cno_matcher = re.compile(r'.*c_no=(\d+)')
    divpage_matcher = re.compile(r'.*divpage=(\d+)')
    
    maxpages_matcher = re.compile(r'.* (\d+)')

    def parse_list(self, pid, page, soup):
        return {}

    def parse_view(self, pid, page, soup):
        return {}

    def parse_write(self, pid, page, soup):
        return {}

    def check_session(self, request, page, soup):
        errcode, errmsg = self.check_error(request, page, soup)
        if errcode == self.ERROR_SIGNED_OUT:
            return False
        
        return True

    def check_error(self, request, page, soup):
        return (None, None)
