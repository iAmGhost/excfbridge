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

from datetime import datetime

from django.db import models

class registry(models.Model):
    session = models.CharField(max_length=36, primary_key=True)
    userid = models.CharField(max_length=20)
    phpsessid = models.CharField(max_length=30)
    signon_time = models.DateTimeField(auto_now_add=True)
    lastactivity_time = models.DateTimeField(auto_now_add=True)

class auditlog(models.Model):
    userid = models.CharField(max_length=20)
    session = models.CharField(max_length=36)
    ipaddress = models.IPAddressField()
    useragent = models.CharField(max_length=300, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

def query(sid):
    if not sid:
        return None
    
    try:
        d = registry.objects.get(session=sid)
    except:
        return None

    return d.userid, d.phpsessid

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

def audit(uid, sid, ip, ua):
    auditlog(userid=uid, session=sid, ipaddress=ip, useragent=ua).save()
    
