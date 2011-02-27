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

import re
from BeautifulSoup import BeautifulSoup

# BeautifulSoup's HTML parsing capability is somewhat problematic, so
# we have to do additional (dirty) shovelling to get the desired result.

class parser:
    ERROR_NONE = 0
    ERROR_SIGNED_OUT = 1
    ERROR_GENERIC = 2

    DECIMAL_MATCHER = re.compile(r'.*(\d+)')

    def parse_list(self, pid, page, soup):
        return {}

    def parse_view(self, pid, page, soup):
        return {}

    def check_session(self, page, soup):
        errcode, errmsg = self.check_error(page, soup)
        if errcode == self.ERROR_SIGNED_OUT:
            return False
        
        return True

    def check_error(self, page, soup):
        return (self.ERROR_NONE, None)

class parser_free(parser):
    """ Parser for free board """

    no_matcher = re.compile(r'.*no=(\d+)')

    def parse_list(self, pid, page, soup):
        output = {}
        alist = []
        output['article_lists'] = alist
        
        trs = filter(lambda x: '<a href="view.php?' in str(x), soup.findAll('tr')[3:])

        for tags in trs:
            title = tags.contents[7].contents[3].contents[2].text.replace('&nbsp;', ' ').replace('/span>', '').strip()
            try:
                comments = tags.contents[7].contents[3].contents[4].text[1:-1]
            except:
                comments = ''
            author = tags.contents[9].getText().replace('/span>', '').strip()
            
            try:
                link = '/view/%s/%s' % (pid, self.no_matcher.match(filter(lambda x: x[0] == 'href', tags.contents[7].contents[3].contents[2].attrs)[0][1]).group(1))
            except:
                link = '#'

            try:
                title = title[title.rindex('>')+1:]
            except:
                pass

            alist.append({'name': title, 'author': author, 'comment': comments, 'link': link})
        
        return output

    def parse_view(self, pid, page, soup):
        output = {}

        cnode = soup.find('span', {'style': 'line-height:160%'})
        cnode.find('div').replaceWith('')

        headers = soup.findAll('tr', {'height': '26'})
        for n in headers:
            if n.contents[3].text == 'Name':
                output['name'] = n.contents[5].contents[0].text
                output['userid'] = n.contents[5].contents[1].strip()[1:-1]
            elif n.contents[3].text == 'Homepage':
                output['homepage'] = n.contents[5].text
            elif n.contents[3].text == 'Subject':
                output['subject'] = n.contents[5].text
        
        output['body'] = cnode.renderContents()
        output['date'] = soup.findAll('table')[2].contents[1].contents[3].getText()

        comments = []
        cmtnodes = soup.findAll('table', {'border': '0', 'align': 'center', 'cellpadding': '2', 'cellspacing': '1', 'width': '100%'})
        for n in cmtnodes:
            cmtnode = {}
            cmtnode['name'] = n.contents[1].contents[1].contents[0].text
            cmtnode['id'] = n.contents[1].contents[1].contents[3].text[1:-1]
            cmtnode['body'] = n.contents[1].contents[5].text
            cmtnode['date'] = n.contents[1].contents[9].contents[0].contents[1].contents[0][1:-1] + ' ' + n.contents[1].contents[9].contents[0].contents[1].contents[2][1:-1]

            comments.append(cmtnode)

        output['comments'] = comments

        return output

    def check_error(self, page, soup):
        try:
            msg = soup.find('tr', {'height': '27', 'align': 'right'}).contents[3].text.strip()
            if not msg:
                return (self.ERROR_NONE, None)
            
            if u'사용권한이 없습니다' in msg:
                return (self.ERROR_SIGNED_OUT, msg)
            else:
                return (self.ERROR_GENERIC, msg)
        except:
            return (self.ERROR_NONE, None)
                
