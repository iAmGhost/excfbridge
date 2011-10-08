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

from flexigate.handlers.index import DEFAULT_INDEX
from flexigate.parsers.common import find_error
from flexigate import registry, remote
from flexigate.tools import *
from settings import TARGET_ENCODING

URL_MENU = 'http://excf.com/menu.html'
URL_SIGN_ON = 'http://excf.com/bbs/login_check.php'
URL_SIGN_OFF = 'http://excf.com/bbs/logout.php?s_url=about:blank'

class SignOnException(Exception):
    pass

def attempt_sign_on(request, response, userid, passwd):
    ip = request.META['REMOTE_ADDR']
    ua = request.META['HTTP_USER_AGENT'] if request.META.has_key('HTTP_USER_AGENT') else None

    encoded = urllib.urlencode(
        {'user_id': userid.encode(TARGET_ENCODING), 'password': passwd, 's_url': 'about:blank'}
    )

    max_age = 365*24*60*60
    expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)

    try:
        sessid = request.COOKIES['session']
    except:
        sessid = generate_session_id()
        response.set_cookie('session', sessid, expires=expires, max_age=max_age)
    
    m = urllib2.urlopen(URL_MENU)
    result, soup = remote.postprocess(m.read())
    errid, errmsg = find_error(result, soup)
    if errid:
        registry.audit(userid, sessid, ip, ua, False, why=errmsg)
        raise SignOnException(error(request, errmsg))

    try:
        phpsessid = re.match('PHPSESSID=([0-9a-f]+)', m.headers['set-cookie']).group(1)
    except:
        registry.audit(userid, sessid, ip, ua, False, why=u'알 수 없음')
        raise SignOnException(error(request, u'사이트 상태가 이상합니다.'))

    l = remote.send_request(request, URL_SIGN_ON, encoded, phpsessid)
    result, soup = remote.postprocess(l.read())

    errid, errmsg = find_error(result, soup)
    if errid:
        registry.audit(userid, sessid, ip, ua, False, why=errmsg)
        raise SignOnException(error(request, errmsg))

    if 'about:blank' in result:
        # succeeded
        registry.register(sessid, userid, phpsessid)
        registry.audit(userid, sessid, ip, ua, True)

        # save form data if needed
        if request.POST.has_key('saveform') and request.POST['saveform'] == 'true':
            response.set_cookie('userid', userid, expires=expires, max_age=max_age)
            response.set_cookie('password', passwd, expires=expires, max_age=max_age)
        else:
            if request.COOKIES.has_key('userid'):
                # clear cookie if deselected
                response.delete_cookie('userid')
                response.delete_cookie('password')

        return True
    else:
        registry.audit(userid, sessid, ip, ua, False, why=u'잘못된 아이디 또는 비밀번호 조합')
        return False

def generate_session_id():
    return uuid.uuid4()

def handle_signon_post(request):
    try:
        userid = request.POST['userid'].decode('utf-8')
        password = request.POST['password']
    except:
        return error(request, u'아이디와 패스워드를 입력해 주시기 바랍니다.', redir='/signon')

    try:
        raddr = request.POST['redirect']
    except:
        raddr = DEFAULT_INDEX

    response = redirect(raddr)

    try:
        if attempt_sign_on(request, response, userid, password):
            return response
        else:
            return error(request, u'로그인에 실패하였습니다.', redir='/signon')
    except SignOnException, e:
        return e.args[0]

def handle_signon_get(request):
    userid = ''
    password = ''
    checked = ''
        
    if request.COOKIES.has_key('userid') and request.COOKIES.has_key('password'):
        userid = request.COOKIES['userid']
        password = request.COOKIES['password']
        checked = "checked='checked'"

    data = default_template_vars(u'sExCF: ExCF for Smartphones', request)
    data['userid'] = userid
    data['password'] = password
    data['saveform'] = checked
    try:
        data['redirect'] = request.GET['redirect']
    except:
        pass

    response = render_to_response('signon.html', data)

    sid = get_session_id(request)
    if not sid:
        sid = generate_session_id()

    max_age = 365*24*60*60
    expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)

    response.set_cookie('session', sid, expires=expires, max_age=max_age)
        
    return response

def handle_signon(request, path = None):
    if request.method == 'GET':
        return handle_signon_get(request)
    else:
        return handle_signon_post(request)

def handle_signoff(request, path = None):
    response = redirect('/signon')

    remote.send_request(request, URL_SIGN_OFF)
    force_sign_out(request, response)

    return response
