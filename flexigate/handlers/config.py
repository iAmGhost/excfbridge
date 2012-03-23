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

from flexigate import pagedefs, remote
from flexigate.tools import *
from flexigate.parsers import common
from flexigate.registry import query, get_prefs, set_prefs
from settings import TARGET_ENCODING, TARGET_SITE

URL_NICKNAME_SET = TARGET_SITE + '/member_modify_ok_nickname.php'

def handle_get(request):
    sess = get_session_id(request)
    prefs = get_prefs(sess)

    data = default_template_vars(u'설정', request)
    data['nickname'] = common.get_my_nickname(request)
    data['prefs'] = prefs

    response = render_to_response('config.html', data)
    
    return response

def handle_post(request):
    sess = get_session_id(request)
    
    if request.POST['domain'] == 'mobile':
        try:
            resize = int(request.POST['resize'])
            if resize < 450:
                resize = 450
        except:
            resize = 1600
        set_prefs(sess, int(request.POST['resize']), request.POST['css'])
    elif request.POST['domain'] == 'global':
        nickname = request.POST['nickname'].encode(TARGET_ENCODING)
        l = remote.send_request(request, URL_NICKNAME_SET, urllib.urlencode({'name': nickname}))
        result, soup = remote.postprocess(l.read())

        redirect_if_not_signed_on(request, result, soup, pagedefs.PAGE_PARSERS['free'])
        
        errcode, errmsg = pagedefs.PAGE_PARSERS['free'].check_error(request, result, soup)
        if errcode:
            return error_forward(request, errmsg)

    return redirect('/config')

def handle(request):
    if request.method == 'GET':
        return handle_get(request)
    else:
        return handle_post(request)
