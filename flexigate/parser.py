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

class parser:
    ERROR_NONE = 0
    ERROR_SIGNED_OUT = 1
    ERROR_GENERIC = 2

    DECIMAL_MATCHER = re.compile(r'.*(\d+)')

    def parse_list(self, pid, page, soup):
        return {}

    def parse_view(self, pid, page, soup):
        return {}

    def check_session(self, page, soup):
        errcode, errmsg = self.check_error(page, soup)
        if errcode == self.ERROR_SIGNED_OUT:
            return False
        
        return True

    def check_error(self, page, soup):
        return (self.ERROR_NONE, None)
