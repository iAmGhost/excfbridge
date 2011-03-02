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

from settings import ADMINS_EXCF
from flexigate import registry, models
from flexigate.tools import *

LIMIT_AUDIT = 100

def handle(request):
    out = registry.query(get_session_id(request))
    
    if not out:
        return error(request, u'로그인되어 있지 않습니다.')
    
    if not out[0] in ADMINS_EXCF:
        return error(request, u'권한이 없습니다.')

    data = default_template_vars(u'관리자 페이지', request)
    data['limit_audit'] = LIMIT_AUDIT
    data['sessions'] = models.registry.objects.order_by('-signon_time').all()
    data['audit'] = models.auditlog.objects.order_by('-time').all()[:LIMIT_AUDIT]
        
    return render_to_response('admin.html', data)
