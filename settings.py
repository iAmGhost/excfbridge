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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# THE SOFTWARE.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_PATH = '/home/segfault/Projects/excfbridge'
SESSION_FLUSH_TRIGGER_PATH = '/tmp/excfbridge_session_flush_trigger2'

ADMINS = (
    ('Park "segfault" Joon-Kyu', 'mastermind@planetmono.org'),
)

MANAGERS = ADMINS

ADMINS_EXCF = ['segfault87', 'excf']
SESSION_EXPIRE = 1800

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = BASE_PATH + '/database/excfbridge.db'

TIME_ZONE = 'Asia/Seoul'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = BASE_PATH + '/static'
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/media/'

SECRET_KEY = 'hhku$j1^-3dl5(!-5+0xeh+9)0@xmnp2jblf5!(ht736v3_hom'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    BASE_PATH+'/templates'
)

INSTALLED_APPS = (
    'excfbridge.flexigate',
)
