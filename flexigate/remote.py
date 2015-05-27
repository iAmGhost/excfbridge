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
import urllib, urllib2

from flexigate import registry
from settings import TARGET_ENCODING

def send_request(request, url, data=None, sessid=None, referer=None):
    if not sessid:
        try:
            lsid = request.COOKIES['session']
            sessid = registry.query(lsid)[1]
        except:
            pass

    headers = {}
    if sessid:
        headers['Cookie'] = 'PHPSESSID=%s' % sessid
    if referer:
        headers['Referer'] = referer

    req = urllib2.Request(url, data, headers)
    return urllib2.urlopen(req)

def postprocess(data):
    # This is dirty fix for missing quotes+non-ascii parameters.
    regex = re.compile(r"(<img src=)(.+?)([ |>])", re.DOTALL)

    data = re.sub(regex, r'\1"\2"\3', data)

    data = data.decode(TARGET_ENCODING, 'ignore')

    return data, BeautifulSoup(data)

