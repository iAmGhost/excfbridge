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

import urllib

from django.shortcuts import redirect, render_to_response

from settings import ADMINS_EXCF
from flexigate import registry
from flexigate.pagedefs import PAGES

def redirect_if_no_session(request):
    # we have to kill inactive session first.
    registry.flush_outdated()

    ret = False

    redir = redirect('/signon?%s' % urllib.urlencode({'redirect': request.path}))

    sid = get_session_id(request)

    if not get_session_id(request):
        ret = True
    elif not registry.query(sid):
        force_sign_out(request, redir)
        ret = True

    if ret:
        return redir

    # there is an activity
    registry.touch(sid)

def redirect_if_not_signed_on(request, page, soup, pagedef):
    if not pagedef.check_session(page, soup):
        # Remote session is expired
        redir = redirect('/signon?%s' % urllib.urlencode({'redirect': request.path})) 
        force_sign_out(request, redir)
        return redir

def get_session_id(request):
    if not request.COOKIES.has_key('session'):
        return None

    return request.COOKIES['session']

def force_sign_out(request, response):
    sid = get_session_id(request)
    
    if sid:
        # Remove item from session storage
        registry.purge(sid)

        # Expire cookie
        response.delete_cookie('session')

def default_template_vars(title, request, location=None):
    out = {}

    out['title'] = title

    try:
        admin = registry.query(get_session_id(request))
        if admin and admin[0] in ADMINS_EXCF:
            out['admin'] = True
            out['signed_on'] = True
            out['user'] = admin[0]
    except:
        pass

    pages = []
    for i in PAGES:
        pages.append({'id': i[0], 'location': i[1], 'name': i[2]})
    out['jumplist'] = pages
    if location:
        out['location'] = location

    return out
    
def error(request, errmsg, redir=None, onclick=None):
    out = default_template_vars(u'오류', request)
        
    attr = 'onclick=\'history.back();\''
    if redir:
        attr = 'href=\'%s\'' % redir
    elif onclick:
        attr = 'onclick=\'%s\'' % redir
        
    out['attr'] = attr
    out['errmsg'] = errmsg

    return render_to_response('error.html', out)

def error_forward(request, errmsg, redir=None, onclick=None):
    return error(request, u'<b>%s</b><br />랩니다.' % errmsg, redir, onclick)

