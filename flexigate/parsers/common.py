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

from flexigate.parser import parser
from flexigate import remote

URL_MENU = 'http://excf.com/menu.html'

def get_sign_on_status(request, page, soup):
    result = remote.send_request(request, URL_MENU)
    html, soup = remote.postprocess(result.read())

    if len(soup.findAll('input', {'type': 'password'})) > 0:
        return False
    else:
        return True

def get_my_nickname(request):
    result = remote.send_request(request, URL_MENU)
    html, soup = remote.postprocess(result.read())
    
    try:
        return soup.find('a', {'onfocus': 'blur()'}).text
    except:
        return None

def find_common_error(page, soup):
    # Traffic check
    title = soup.find('title', text=u'트래픽초과안내')
    if title:
        return (parser.ERROR_THROTTLE_LIMIT, u'트래픽 오버입니다.')

    return None

def find_error(page, soup):
    res = find_common_error(page, soup)
    if res:
        return res

    return (None, None)
