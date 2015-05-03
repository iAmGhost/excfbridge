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

import urllib, urllib2
import re

from django.shortcuts import render_to_response

from flexigate import remote, pagedefs
from flexigate.parser import parser
from flexigate.parsers import common, inbox_sent
from flexigate.parsers.common import find_error
from flexigate.tools import *
from settings import TARGET_ENCODING, TARGET_SITE

URL = TARGET_SITE + '/zboard.php'

URL_ADULT_CHECK = TARGET_SITE + '/agecheck.php'
URL_MENU = 'http://excf.com/menu.php'

class AdultCheckException(Exception):
    pass

def attempt_adult_check(request, response, ssn1, ssn2):
    ip = request.META['REMOTE_ADDR']
    if ip == '127.0.0.1':
        ip = request.META['HTTP_X_REAL_IP']
    ua = request.META['HTTP_USER_AGENT'] if request.META.has_key('HTTP_USER_AGENT') else None

    encoded = urllib.urlencode(
        {'resno1': ssn1.encode(TARGET_ENCODING), 'resno2': ssn2.encode(TARGET_ENCODING),
         'redirect_to': '/bbs/zboard.php?id=ddf'.encode(TARGET_ENCODING)}
    )

    # user is already logged in this moment.
    userid, phpsessid = registry.query(request.COOKIES['session'])

    l = remote.send_request(request, URL_ADULT_CHECK, encoded, phpsessid)

    result, soup = remote.postprocess(l.read())

    # meh.
    if u"잘못된 주민등록번호입니다." in result:
        return False
    else:
        return True

def redirect_if_not_signed_on(request, page, soup):
    print type(page)
    if u'alert("로그인된 회원만이 사용할수 있습니다");' in page:
        # Remote session is expired
        redir = redirect('/signon?%s' % urllib.urlencode({'redirect': request.path})) 
        force_sign_out(request, redir)
        raise redirection(redir)

def handle_adult_check(request):
    if request.method == 'GET':
        return handle_adult_check_get(request)
    else:
        return handle_adult_check_post(request)

def handle_adult_check_get(request):
    try:
        redirect_if_no_session(request)

        try:
            page = int(args[0])
        except:
            page = 1

        query = URL + '?page=%d' % page
        result = remote.send_request(request, query)
        html, soup = remote.postprocess(result.read())

        data = default_template_vars(u'성인인증', request, 'that')
        data['redirect'] = request.GET.get('redirect', None)

        redirect_if_not_signed_on(request, html, soup)

        return render_to_response('adult_check.html', data)
    except redirection, e:
        return e.where

def handle_adult_check_post(request):
    ssn1 = request.POST.get('ssn1', None)
    ssn2 = request.POST.get('ssn2', None)

    if ssn1 is None or ssn2 is None:
        return error(request, u'주민번호를 입력해주시기 바랍니다.', redir='/adult_check')

    try:
        raddr = request.POST['redirect']
    except:
        raddr = "/list/that"

    response = redirect(raddr)

    try:
        if attempt_adult_check(request, response, ssn1, ssn2):
            return response
        else:
            return error(request, u'잘못된 주민등록번호입니다.', redir='/adult_check')
    except AdultCheckException, e:
        return e.args[0]
