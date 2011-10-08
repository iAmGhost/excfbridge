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

def useragent(ua):
    if 'Chrom' in ua:
        return 'Google Chrome'
    elif 'Firefox' in ua:
        return 'Mozilla Firefox'
    elif 'MSIE 6.0' in ua:
        return u'Internet Explorer 6'
    elif 'MSIE 7.0' in ua:
        return u'Internet Explorer 7'
    elif 'MSIE 8.0' in ua:
        return u'Internet Explorer 8'
    elif 'MSIE' in ua:
        return u'Internet Explorer'
    elif 'Opera Mobi' in ua:
        return u'Opera Mobile'
    elif 'Opera' in ua:
        return u'Opera'
    elif 'iPod' in ua:
        return u'iPod'
    elif 'iPhone' in ua:
        return u'iPhone'
    elif 'Android' in ua:
        return u'Android'
    elif 'Skyfire' in ua:
        return u'Skyfire'
    elif 'SymbianOS' in ua:
        return u'SymbianOS'
    elif 'Safari' in ua:
        return u'Safari'
    else:
        return u'Unknown Agent'

def elapsed(a, b):
    delta = (a - b).seconds
    days = (a - b).days

    out = []
    if days > 0:
        out.append('%dd' % days)
    if delta > 3600:
        hours = delta / 3600
        out.append('%dh' % hours)
        delta -= hours * 3600
    if delta > 60:
        minutes = delta / 60
        out.append('%dm' % minutes)
        delta -= minutes * 60
    if delta > 0:
        out.append('%ds' % delta)

    if len(out) == 0:
        out.append('0s')

    return ' '.join(out)

class registry(models.Model):
    session = models.CharField(max_length=36, primary_key=True)
    userid = models.CharField(max_length=20)
    phpsessid = models.CharField(max_length=30)
    signon_time = models.DateTimeField(auto_now_add=True)
    lastactivity_time = models.DateTimeField(auto_now_add=True)

    def active_usage(self):
        return elapsed(self.lastactivity_time, self.signon_time)
    
    def elapsed(self):
        return elapsed(datetime.now(), self.signon_time)

class faillog(models.Model):
    userid = models.CharField(max_length=20)
    ipaddress = models.IPAddressField()
    useragent = models.CharField(max_length=300, null=True, blank=True)
    reason = models.CharField(max_length=100, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def browser(self):
        return useragent(self.useragent)

class auditlog(models.Model):
    userid = models.CharField(max_length=20)
    session = models.CharField(max_length=36)
    ipaddress = models.IPAddressField()
    useragent = models.CharField(max_length=300, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def browser(self):
        return useragent(self.useragent)
    
