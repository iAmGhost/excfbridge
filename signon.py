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

import datetime
import urllib, urllib2
import re
import uuid
from Cookie import SimpleCookie

from page import page
from index import index
import registry
import remote

class signon(page):
    """ Main entrypoint for signing on to ExCF """

    URL_MENU = 'http://excf.com/menu.html'
    URL_SIGN_ON = 'http://excf.com/bbs/login_check.php'

    def attempt_sign_on(self, userid, passwd):
        encoded = urllib.urlencode(
            {'user_id': userid.encode('cp949'), 'password': passwd, 's_url': 'about:blank'}
        )

        sessid = self.request.cookies['session']
        if not sessid:
            sessid = self.generate_session_id()
            self.response.headers.add_header('Set-cookie', 'session=%s; path=/' % sessid)
        
        m = urllib2.urlopen(self.URL_MENU)
        phpsessid = re.match('PHPSESSID=([0-9a-f]+)', m.headers['set-cookie']).group(1)

        l = remote.send_request(self, self.URL_SIGN_ON, encoded, phpsessid)
        result = remote.postprocess(l.read())

        if 'about:blank' in result:
            # succeeded
            ip = self.request.remote_addr
            ua = self.request.headers['User-Agent'] if self.request.headers.has_key('User-Agent') else None

            registry.register(sessid, phpsessid)
            registry.audit(userid, sessid, ip, ua)

            # save form data if needed
            if self.request.get('saveform'):
                self.response.headers.add_header('Set-cookie', 'userid=%s; path=/signon' % userid)
                self.response.headers.add_header('Set-cookie', 'password=%s; path=/signon' % passwd)
            else:
                if self.request.cookies.has_key('userid'):
                    # clear cookie if deselected
                    dtime = datetime.datetime.now() - datetime.timedelta(hours=1)
                    dtimestr = dtime.strftime("%a, %d-%b-%Y %H:%M:%S GMT")

                    self.response.headers.add_header('Set-cookie', 'userid=; path=/signon; expires=%s' % dtimestr)
                    self.response.headers.add_header('Set-cookie', 'password=; path=/signon; expires=%s' % dtimestr)

            return True
        else:
            return False

    def generate_session_id(self):
        return uuid.uuid4()

    def post(self):
        userid = self.request.get('userid').decode('utf-8')
        password = self.request.get('password')

        redirect = self.request.get('redirect')
        if not redirect:
            redirect = index.DEFAULT_INDEX

        if self.attempt_sign_on(userid, password):
            self.redirect(redirect)
        else:
            self.error(u'로그인에 실패하였습니다.', redir='/signon')

    def get(self):
        userid = ''
        password = ''
        checked = ''
        
        if self.request.cookies.has_key('userid') and self.request.cookies.has_key('password'):
            userid = self.request.cookies['userid']
            password = self.request.cookies['password']
            checked = "checked='checked'"

        if not self.get_session_id():
            self.response.headers.add_header('Set-cookie', 'session=%s; path=/' % self.generate_session_id())
        
        self.set_title(u'로그인')
        self.render('signon.html.frag', {'userid': userid, 'password': password, 'saveform': checked})
