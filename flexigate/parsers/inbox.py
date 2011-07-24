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

from flexigate import remote, pagedefs
from flexigate.parsers import common
from flexigate.parser import no_matcher

def parse_list(page, soup):
    data = {}

    m = soup.findAll('tr', {'onmouseover': 'this.style.backgroundColor="#FFF5F5"'})
    messages = []
    for msg in m:
        item = {}
        if msg.contents[3].contents[0]['src'] == u'images/memo_unread.gif':
            item['unread'] = True

        item['topic'] = msg.contents[5].text
        item['link'] = '/inbox/view/%d' % int(no_matcher.match(msg.contents[5].contents[3]['href']).group(1))
        item['sender'] = msg.contents[7].contents[3].text

        messages.append(item)
    data['message_lists'] = messages

    pages = soup.findAll('table', {'cellpadding': '5'})[1].text.replace('&nbsp;', '')
    data['maxpages'] = int(pages.replace('[', ' ').replace(']', ' ').strip().split()[-1])

    return data
    
def parse_view(page, soup):
    data = {}

    body = soup.findAll('table', {'width': '100%', 'border': '0', 'cellspacing': '0', 'cellpadding': '0'})[2].findAll('tr')

    data['name'] = body[1].contents[3].contents[3].text
    data['userid'] = body[1].contents[3].contents[5].contents[2][3:-1]
    data['topic'] = body[3].text
    data['date'] = body[5].text

    body_ = body[7].contents[3]
    body_.contents[0].replaceWith('')
    data['body'] = body_.renderContents()

    uidlink = body[8].contents[3].contents[0]['href']
    data['uid'] = int(no_matcher.match(uidlink).group(1))

    return data

def parse_new(page, soup):
    data = {}

    namestr = soup.find('font', {'color': 'brown'}).text.split()
    data['name'] = namestr[1].replace('&nbsp;', '')[1:-1]
    data['userid'] = namestr[0]

    return data
