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

from google.appengine.ext import db

class registry(db.Model):
    phpsessid = db.StringProperty(required=True)
    signon_time = db.DateTimeProperty(auto_now_add=True)

class auditlog(db.Model):
    userid = db.StringProperty(required=True)
    session = db.StringProperty(required=True)
    ipaddress = db.StringProperty(required=True)
    useragent = db.StringProperty()
    time = db.DateTimeProperty(auto_now_add=True)

def query(sid):
    d = registry.get_by_key_name(sid)
    if not d:
        return None

    return d.phpsessid

def register(sid, psess):
    r = registry(key_name=sid, phpsessid=psess)
    d = registry.get_by_key_name(sid)
    if d:
        d.delete()
        
    r.put()

def purge(sid):
    d = registry.get_by_key_name(sid)
    if d:
        d.delete()

def audit(uid, sid, ip, ua):
    auditlog(userid=uid, session=sid, ipaddress=ip, useragent=ua).put()
    
