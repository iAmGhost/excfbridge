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

from flexigate.parsers.excf_new import parser_object as excf_new

PAGE_IDS = {
    'free': 'free3',
    'general': 'opin',
    'creation': 'cre1',
    'cartoon': 'gene1',
    'playground': 'ev',
    'game': 'game',
    'eatball': 'eatball',
    'that': 'ddf',
}

PAGE_NAMES = {
    'free': u'자유 게이판',
    'general': u'다용도 게시판',
    'creation': u'창작 게시판',
    'cartoon': u'만화 게시판',
    'playground': u'놀이 게시판',
    'game': u'오락실',
    'inbox': u'쪽지함',
    'inbox_sent': u'보낸 쪽지함',
    'eatball': u'먹',
    'that': u'그게시판',
}

PAGE_PARSERS = {
    'free': excf_new,
    'general': excf_new,
    'creation': excf_new,
    'cartoon': excf_new,
    'playground': excf_new,
    'game': excf_new,
    'eatball': excf_new,
    'that': excf_new,
}

PAGES = (
    ('free', '/list/free', PAGE_NAMES['free']),
    ('general', '/list/general', PAGE_NAMES['general']),
    ('creation', '/list/creation', PAGE_NAMES['creation']),
    ('cartoon', '/list/cartoon', PAGE_NAMES['cartoon']),
    ('playground', '/list/playground', PAGE_NAMES['playground']),
    ('game', '/list/game', PAGE_NAMES['game']),
    ('eatball', '/list/eatball', PAGE_NAMES['eatball']),
    ('that', '/list/that', PAGE_NAMES['that']),
    ('inbox', '/inbox', PAGE_NAMES['inbox']),
    ('inbox_sent', '/inbox_sent', PAGE_NAMES['inbox_sent']),
)
