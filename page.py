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
import os
import urllib
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import config
import registry

class page(webapp.RequestHandler):
    """ Base class for every page 'handler's. """

    title = ''

    def set_title(self, title):
        self.title = title

    def redirect_if_no_session(self):
        if not self.get_session_id():
            self.redirect('/signon?%s' % urllib.urlencode({'redirect': self.request.path}))
            return True
        elif not registry.query(self.get_session_id()):
            self.force_sign_out()
            self.redirect('/signon?%s' % urllib.urlencode({'redirect': self.request.path}))
            return True
        
        return False                                 

    def redirect_if_not_signed_on(self, page, soup, pagedef):
        if not pagedef.check_session(page, soup):
            # Remote session is expired
            self.force_sign_out()
            self.redirect('/signon?%s' % urllib.urlencode({'redirect': self.request.path}))
            return True
        
        return False

    def get_session_id(self):
        if not self.request.cookies.has_key('session'):
            return None

        return self.request.cookies['session']

    def force_sign_out(self):
        sid = self.get_session_id()

        if sid:
            # Remove item from session storage
            registry.purge(sid)

            # Expire cookie
            dtime = datetime.datetime.now() - datetime.timedelta(hours=1)
            dtimestr = dtime.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
            self.response.headers.add_header('Set-cookie', 'session=; path=/; expires=%s' % dtimestr)

    # Show error message
    def error(self, errmsg, redir=None, onclick=None):
        self.set_title(u'오류')
        
        attr = 'onclick=\'history.back();\''
        if redir:
            attr = 'href=\'%s\'' % redir
        elif onclick:
            attr = 'onclick=\'%s\'' % redir
        
        var = {}
        var['attr'] = attr
        var['errmsg'] = errmsg

        self.render('error.html.frag', var)

    def error_forward(self, errmsg, redir=None, onclick=None):
        self.error(u'<b>%s</b><br />랩니다.' % errmsg, redir, onclick)

    # Construct HTML
    def render(self, filename, attributes):
        dirname = os.path.dirname(__file__) + '/templates'

        headervals = {'title': self.title}
        footervals = {}
        
        try:
            admin = registry.query(self.get_session_id())
            if admin and admin[0] in config.ADMINISTRATORS:
                footervals['admin'] = True
                headervals['signed_on'] = True
                headervals['user'] = admin[0]
        except:
            pass

        header = os.path.join(dirname, 'header.html.frag')
        body = os.path.join(dirname, filename)
        footer = os.path.join(dirname, 'footer.html.frag')

        self.response.headers.add_header('Content-Type', 'text/html')
        self.response.out.write(template.render(header, headervals))
        self.response.out.write(template.render(body, attributes))
        self.response.out.write(template.render(footer, footervals))
        
