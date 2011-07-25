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

from base64 import b64decode
from urllib import unquote_plus
import re

from settings import TARGET_ENCODING

def parse_layer_info(script):
    output = {}

    for line in script.split('\n'):
        line = line.strip()
        if not line.startswith('print_ZBlayer'):
            continue

        splitinfo = line.split()

        number = int(splitinfo[0][22:-2])

        item = {}
        item['user_no'] = int(splitinfo[3][1:-2])
        item['user_name'] = unquote_plus(str(splitinfo[5][1:-2])).decode(TARGET_ENCODING, 'ignore').replace('\'', '\\\'')
        item['user_website'] = unquote_plus(str(splitinfo[1][1:-2])).decode(TARGET_ENCODING, 'ignore').replace('\'', '\\\'')
        item['user_email'] = b64decode(str(splitinfo[2][1:-2])).decode(TARGET_ENCODING, 'ignore').replace('\'', '\\\'')

        output[number] = item

    return output

def postprocess_string(text):
    return text.replace('&nbsp;', ' ').strip().replace('/span>', '')

find_attr = lambda node, attr: filter(lambda x: x[0] == attr, node.attrs)[0][1]

decimal_matcher = re.compile(r'.*?(\d+)')
no_matcher = re.compile(r'.*no=(\d+)')
cno_matcher = re.compile(r'.*c_no=(\d+)')
divpage_matcher = re.compile(r'.*divpage=(\d+)')
    
maxpages_matcher = re.compile(r'.* (\d+)')

class parser:
    ERROR_SIGNED_OUT = 1
    ERROR_THROTTLE_LIMIT = 2
    ERROR_GENERIC = 3

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
