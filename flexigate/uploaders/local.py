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

import os
from hashlib import md5
from urllib import quote
import Image

from flexigate.tools import *
from settings import UPLOAD_LOCAL_PATH, UPLOAD_LOCAL_URL, UPLOAD_LOCAL_SIZE, TARGET_ENCODING

def resize(filename):
    im = Image.open(filename)
    
    size = im.size
    if size[0] < UPLOAD_LOCAL_SIZE and size[1] < UPLOAD_LOCAL_SIZE:
        return

    if size[0] > size[1]:
        nx = UPLOAD_LOCAL_SIZE
        ny = int(size[1] * (float(UPLOAD_LOCAL_SIZE) / size[0]))
    else:
        nx = int(size[0] * (float(UPLOAD_LOCAL_SIZE) / size[1]))
        ny = UPLOAD_LOCAL_SIZE

    im = im.resize((nx, ny), Image.ANTIALIAS)
    im.save(filename, quality=90)

def upload(request, fileobj):
    sid = md5(get_session_id(request)).hexdigest()

    retrycnt = 0
    while True:
        if retrycnt == 0:
            filename = '%s_%s' % (sid, fileobj.name)
        else:
            filename = '%s_%d_%s' % (sid, retrycnt, fileobj.name)
        filename = filename.encode('utf-8')
        fpath = '%s/%s' % (UPLOAD_LOCAL_PATH, filename)

        if not os.path.exists(fpath):
            break
        
        retrycnt += 1 
     
    f = open(fpath, 'wb+')
    for chunk in fileobj.chunks():
        f.write(chunk)
    f.close()

    resize(fpath)

    return '%s/%s' % (UPLOAD_LOCAL_URL, quote(filename))
    
