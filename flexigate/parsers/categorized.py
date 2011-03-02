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

from flexigate.parser import parser as parser_base, postprocess_string

class parser(parser_base):
    no_matcher = re.compile(r'.*no=(\d+)')

    def parse_list(self, pid, page, soup):
        output = {}
        alist = []
        output['article_lists'] = alist
        
        trs = soup.findAll('tr', {'align': 'center', 'onmouseover': 'this.style.backgroundColor=\'#F5F5F5\''})

        for tags in trs:
            dtitle = tags.contents[6].contents[5].text
            try:
                dtitle = dtitle[dtitle.rindex('>')+1:]
            except:
                pass

            title = '[%s] %s' %  (tags.contents[4].text, dtitle)
            try:
                comments = tags.contents[6].contents[7].text[1:-1]
            except:
                comments = ''
            author = tags.contents[8].text
            
            try:
                link = '/view/%s/%s' % (pid, self.no_matcher.match(filter(lambda x: x[0] == 'href', tags.contents[6].contents[5].attrs)[0][1]).group(1))
            except:
                link = '#'

            alist.append({'name': title, 'author': author, 'comment': comments, 'link': link})
        
        return output

    def parse_view(self, pid, page, soup):
        output = {}

        headers = soup.find('table', {'bgcolor': '#EFEFEF'}).findAll('tr')
        for n in headers:
            if 'Name' in n.contents[1].text:
                output['name'] = n.contents[3].contents[0].contents[0].text
                output['userid'] = n.contents[3].contents[0].contents[1].strip()[1:-1]
            elif 'Home' in n.contents[1].text:
                output['homepage'] = n.contents[3].text
            elif 'Subject' in n.contents[1].text:
                output['subject'] = n.contents[3].text

        
        body = soup.find('span', {'style': 'line-height:160%'})
        body.find('div').replaceWith('')
        output['body'] = body.renderContents()

        comments = []
        cmtnodes = soup.findAll('table', {'border': '0', 'cellspacing': '0', 'cellpadding': '0', 'width': '95%'})[4].findAll('tr', {'align': 'center'})
        for n in cmtnodes[:-1]:
            cmtnode = {}
            cmtnode['name'] = postprocess_string(n.contents[1].contents[0].text)
            cmtnode['body'] = postprocess_string(n.contents[7].text)
            date = map(lambda x: x[:-1], n.contents[3].contents[0].contents[1].attrs[0][1].split())
            cmtnode['date'] = '%s/%s %s:%s:%s' % (date[1], date[2], date[3], date[4], date[5])

            comments.append(cmtnode)

        output['comments'] = comments

        return output

    def check_error(self, page, soup):
        try:
            msg = soup.find('td').find('font', {'color': 'red'}).text.strip()
            if not msg:
                return (self.ERROR_NONE, None)
            
            if u'사용권한이 없습니다' in msg:
                return (self.ERROR_SIGNED_OUT, msg)
            else:
                return (self.ERROR_GENERIC, msg)
        except:
            return (self.ERROR_NONE, None)

parser_object = parser()
