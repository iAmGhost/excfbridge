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

from django.shortcuts import redirect

import random

def handle(request):
    response = redirect('/')

    #if request.COOKIES.has_key('aprilfools'):
    #    response.delete_cookie('aprilfools')
    #else:
    #    response.set_cookie('aprilfools', '1')

    return response

def manuzelize(instr):
    if type(instr) == unicode:
        isunicode = True
        u = instr.strip()
    else:
        isunicode = False
        u = instr.decode('utf-8').strip()
    u = u.replace('<br />', '\n').replace('<br>', '\n').replace('<BR>', '\n')

    output = []
    
    for j in u.split('\n'):
        j = j.strip()

        if len(j) == 0:
            output.append('')
            continue

        trailing = u''
        for k in j[::-1]:
            if k == u'.' or k == u'!' or k == u'?' or k == u' ' or k == u';':
                trailing += k
            else:
                break

        trailing = trailing[::-1]
        heart = random.choice([u'♥', u'♡'])

        if len(trailing) > 0:
            line = j[:-len(trailing)]
        else:
            line = j
        for i in range(random.randrange(3)+1):
            line += heart

        output.append(line)
    
    ostr = u'<br />'.join(output)

    if isunicode:
        return ostr
    else:
        return ostr.encode('utf-8')
