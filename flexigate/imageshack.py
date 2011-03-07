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

from BeautifulSoup import BeautifulStoneSoup
import pycurl

from settings import IMAGESHACK_API_KEY

class response_handler:
    def __init__(self):
        self.contents = ''

    def write(self, buf):
        self.contents = self.contents + buf

def upload(filename):
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    c.setopt(c.URL, 'http://www.imageshack.us/upload_api.php')

    opts = []
    opts.append(('fileupload', (c.FORM_FILE, filename.encode('utf-8'))))
    opts.append(('key', IMAGESHACK_API_KEY.encode('utf-8')))
    opts.append(('optimage', '1'))
    opts.append(('optsize', '1280x1280'))
    c.setopt(c.HTTPPOST, opts)
    cb = response_handler()
    c.setopt(c.WRITEFUNCTION, cb.write)
    c.perform()

    try:
        return BeautifulStoneSoup(cb.contents).find('image_link').renderContents()
    except:
        return None
