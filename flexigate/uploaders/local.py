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
from PIL import Image
from PIL.ExifTags import TAGS

from flexigate.tools import *
from settings import UPLOAD_LOCAL_PATH, UPLOAD_LOCAL_URL, UPLOAD_LOCAL_SIZE, TARGET_ENCODING

def rotate(img):
    try:
        exif = img._getexif()
    except:
        return img

    if not exif or not exif.items:
        return img

    for tag, value in exif.items():
        decoded = TAGS.get(tag, tag)
        if decoded == 'Orientation':
            if value == 1:
                return img
            elif value == 2:
                return img.transpose(Image.FLIP_LEFT_RIGHT)
            elif value == 3:
                return img.transpose(Image.ROTATE_180)
            elif value == 4:
                return img.transpose(Image.FLIP_TOP_BOTTOM)
            elif value == 5:
                return img.transpose(Image.ROTATE_90).transpose(Image.FLIP_LEFT_RIGHT)
            elif value == 6:
                return img.transpose(Image.ROTATE_270)
            elif value == 7:
                return img.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)
            elif value == 8:
                return img.transpose(Image.ROTATE_90)
            else:
                return img

    return img

def resize(filename, resize):
    if resize == 0:
        return

    im = Image.open(filename)
    if not im:
        return

    im = rotate(im)
   
    size = im.size

    if size[0] < resize and size[1] < resize:
        return

    if size[0] > size[1]:
        nx = resize
        ny = int(size[1] * (float(resize) / size[0]))
    else:
        nx = int(size[0] * (float(resize) / size[1]))
        ny = resize

    im = im.resize((nx, ny), Image.ANTIALIAS)
    im.save(filename, quality=90)

def upload(request, fileobj, size, sid = None, bid = None, uid = None):
    if not sid:
        sid = md5(get_session_id(request)).hexdigest()

    prefix = ''
    if bid is not None and uid is not None:
        if not os.path.exists('%s/%s' % (UPLOAD_LOCAL_PATH, bid)):
            os.mkdir('%s/%s' % (UPLOAD_LOCAL_PATH, bid))
        if not os.path.exists('%s/%s/%s' % (UPLOAD_LOCAL_PATH, bid, uid)):
            os.mkdir('%s/%s/%s' % (UPLOAD_LOCAL_PATH, bid, uid))
        prefix = '%s/%s/' % (bid, uid)

    retrycnt = 0
    while True:
        if retrycnt == 0:
            filename = prefix + '%s_%s' % (sid, fileobj.name)
        else:
            filename = prefix + '%s_%d_%s' % (sid, retrycnt, fileobj.name)
        filename = filename.encode('utf-8')
        fpath = '%s/%s' % (UPLOAD_LOCAL_PATH, filename)

        if not os.path.exists(fpath):
            break
        
        retrycnt += 1 
     
    f = open(fpath, 'wb+')
    for chunk in fileobj.chunks():
        f.write(chunk)
    f.close()

    resize(fpath, size)

    return '%s/%s' % (UPLOAD_LOCAL_URL, quote(filename))
    
