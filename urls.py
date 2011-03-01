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

from django.conf.urls.defaults import *

from flexigate.handlers.admin import handle as admin
from flexigate.handlers.index import handle as index
from flexigate.handlers.list import handle as listing
from flexigate.handlers.post import handle_article as post, handle_comment as post_comment
from flexigate.handlers.signon import handle_signon as signon, handle_signoff as signoff
from flexigate.handlers.view import handle as view

urlpatterns = patterns('',
    (r'^$', index),
    (r'^admin$', admin),
    (r'^signon$', signon),
    (r'^signoff$', signoff),
    (r'^list/(.*)$', listing),
    (r'^post/(.*)$', post),
    (r'^post_comment/(.*)$', post_comment),
    (r'^view/(.*)$', view),
)



