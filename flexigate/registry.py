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

from datetime import datetime, timedelta
import pickle

from settings import SESSION_EXPIRE, SESSION_FLUSH_TRIGGER_PATH
from flexigate.models import registry, auditlog, faillog, prefs

def query(sid):
    if not sid:
        return None
    
    try:
        d = registry.objects.get(session=sid)
    except:
        return None

    return d.userid, d.phpsessid

def get_prefs(sid):
    try:
        uid = query(sid)[0]
        try:
            return prefs.objects.get(userid=uid)
        except:
            return prefs(userid=uid)
    except:
        return None

def set_prefs(sid, photo_resize, template):
    try:
        o = get_prefs(sid)
        o.photo_resize = photo_resize
        o.template = template
        o.save()
    except:
        return False

    return True

def touch(sid):
    if not sid:
        return

    try:
        d = registry.objects.get(session=sid)
    except:
        return

    d.lastactivity_time = datetime.now()
    d.save()

def register(sid, userid, psess):
    r = registry(session=sid, userid=userid, phpsessid=psess)
    try:
        registry.objects.get(session=sid).delete()
    except:
        pass
        
    r.save()

def purge(sid):
    if not sid:
        return

    try:
        registry.objects.get(session=sid).delete()
    except:
        pass

def flush_outdated():
    try:
        trigger = pickle.loads(open(SESSION_FLUSH_TRIGGER_PATH, 'r').read())
    except:
        trigger = datetime.now() - timedelta(seconds=1)

    if datetime.now() > trigger:
        registry.objects.filter(lastactivity_time__lte=datetime.now()-timedelta(seconds=SESSION_EXPIRE)).delete()

        open(SESSION_FLUSH_TRIGGER_PATH, 'w').write(pickle.dumps(datetime.now() + timedelta(minutes=5)))

def audit(uid, sid, ip, ua, success=True, why=''):
    if success:
        auditlog(userid=uid, session=sid, ipaddress=ip, useragent=ua).save()
    else:
        faillog(userid=uid, ipaddress=ip, useragent=ua, reason=why).save()

