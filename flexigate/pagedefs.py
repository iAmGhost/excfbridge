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

from flexigate.parsers import uncategorized, categorized

PAGE_IDS = {
    'free': 'free3',
    'general': 'opin',
    'creation': 'cre1',
    'cartoon': 'gene1',
    'playground': 'ev',
    'game': 'game',
}

PAGE_NAMES = {
    'free': u'자유 게시판',
    'general': u'다용도 게시판',
    'creation': u'창작 게시판',
    'cartoon': u'만화 게시판',
    'playground': u'놀이 게시판',
    'game': u'오락실',
}

PAGE_PARSERS = {
    'free': uncategorized.parser_object,
    'general': categorized.parser_object,
    'creation': categorized.parser_object,
    'cartoon': uncategorized.parser_object,
    'playground': uncategorized.parser_object,
    'game': categorized.parser_object,
}
