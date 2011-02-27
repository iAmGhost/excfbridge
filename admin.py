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

from page import page
import registry

class admin(page):
    ALLOWED_USER = ['segfault87', 'excf']

    LIMIT_REGISTRY = 250
    LIMIT_AUDIT = 500

    def get(self):
        out = registry.query(self.get_session_id())
        
        if not out:
            self.error(u'로그인되어 있지 않습니다.')
            return

        if not out[0] in self.ALLOWED_USER:
            self.error(u'권한이 없습니다.')

        outvars = {}
        outvars['limit_registry'] = self.LIMIT_REGISTRY
        outvars['limit_audit'] = self.LIMIT_AUDIT
        outvars['sessions'] = registry.registry.all().order('-signon_time').fetch(self.LIMIT_REGISTRY)
        outvars['audit'] = registry.auditlog.all().order('-time').fetch(self.LIMIT_AUDIT)
        
        self.set_title(u'접속 기록')
        self.render('admin.html.frag', outvars)
