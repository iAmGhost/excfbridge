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

from flexigate.parser import *
from flexigate.parsers.common import *

class parser(parser):
    def parse_list(self, pid, page, soup):
        output = {}
        alist = []
        output['article_lists'] = alist

        zbllist = parse_layer_info(soup.findAll('script')[3].text)
        
        if 'memo_on.swf' in page:
            output['new_privmsg'] = True
        
        pages = soup.findAll('td', {'valign': 'absbottom'})[0]

        maxpages = 1

        for pagelink in pages.findAll('a'):
            if pagelink.text == u'[계속 검색]':
                output['divnext'] = int(divpage_matcher.match(find_attr(pagelink, 'href')).group(1))
            elif pagelink.text == u'[이전 검색]':
                output['divprev'] = int(divpage_matcher.match(find_attr(pagelink, 'href')).group(1))
        
        for page in pages.findAll('font'):
            try:
                pnum = int(decimal_matcher.match(page.text).group(1))
                if pnum > maxpages:
                    maxpages = pnum
            except:
                pass
        output['maxpages'] = maxpages
        
        trs = soup.findAll('tr', {'align': 'center', 'valign': 'middle', 'height': '26'})

        cnt = 1
        for tags in trs:
            title = postprocess_string(tags.contents[7].contents[3].contents[2].text)
            comments = ''
            if not title:
                title = postprocess_string(tags.contents[7].contents[3].text)
                if title.endswith(']'):
                    comments = title[title.rfind('[')+1:title.rfind(']')]
                    title = title[:title.rfind('[')]

            try:
                comments = tags.contents[7].contents[3].contents[4].text[1:-1]
            except:
                pass
            
            try:
                author = tags.contents[9].getText().replace('/span>', '').strip()
            except:
                author = ''
            
            try:
                link = '/view/%s/%s' % (pid, no_matcher.match(find_attr(tags.contents[7].contents[3].contents[2], 'href')).group(1))
            except:
                link = '#'

            try:
                title = title[title.rindex('>')+1:]
            except:
                pass

            nitem = {'name': title, 'author': author, 'comment': comments, 'link': link}
            if zbllist.has_key(cnt):
                nitem.update(zbllist[cnt])

            alist.append(nitem)
            cnt += 1
        
        return output

    def parse_view(self, pid, page, soup):
        output = {}

        zbllist = parse_layer_info(soup.findAll('script')[1].text)

        if 'memo_on.swf' in page:
            output['new_privmsg'] = True

        cnode = soup.find('span', {'style': 'line-height:160%'})
        try:
            cnode.find('div').replaceWith('')
        except:
            pass

        headers = soup.findAll('tr', {'height': '26'})
        for n in headers:
            if n.contents[3].text == 'Name':
                output['name'] = n.contents[5].contents[0].text
                output['userid'] = n.contents[5].contents[1].strip()[1:-1]
            elif n.contents[3].text == 'Homepage':
                output['homepage'] = n.contents[5].text
            elif n.contents[3].text == 'Subject':
                output['subject'] = n.contents[5].text

        if zbllist.has_key(3):
            output.update(zbllist[3])
        
        output['body'] = cnode.renderContents()
        output['date'] = soup.findAll('table')[2].contents[1].contents[3].getText()

        if len(soup.findAll('input', {'type': 'text'})) == 0:
            output['nocomments'] = True
        if soup.find('a', text='Write') and soup.find('a', text='Modify'):
            output['modify'] = True

        comments = []
        cmtnodes = soup.findAll('table', {'border': '0', 'align': 'center', 'cellpadding': '2', 'cellspacing': '1', 'width': '100%'})
        cnt = 4
        for n in cmtnodes:
            cmtnode = {}
            cmtnode['name'] = postprocess_string(n.contents[1].contents[1].contents[0].text)
            cmtnode['id'] = n.contents[1].contents[1].contents[3].text[1:-1]
            cmtnode['body'] = postprocess_string(n.contents[1].contents[5].renderContents())
            cmtnode['date'] = n.contents[1].contents[9].contents[0].contents[1].contents[0][1:-1] + ' ' + n.contents[1].contents[9].contents[0].contents[1].contents[2][1:-1]
            try:
                cmtnode['did'] = cno_matcher.match(find_attr(n.contents[1].contents[7].contents[0], 'href')).group(1)
            except:
                pass

            if zbllist.has_key(cnt):
                cmtnode.update(zbllist[cnt])

            comments.append(cmtnode)
            cnt += 1

        output['comments'] = comments

        return output

    def check_write(self, pid, page, soup):
        output = {}

        try:
            output['subject'] = filter(lambda x: x[0] == 'value', soup.find('input', {'type': 'text', 'name': 'subject'}).attrs)[0][1]
            output['contents'] = soup.find('textarea', {'name': 'memo'}).text
        except:
            pass

        return output

    def check_error(self, request, page, soup):
        try:
            error = find_common_error(page, soup)
            if error:
                return error

            msg = soup.find('tr', {'height': '27', 'align': 'right'}).contents[3].text.strip()
            if not msg:
                return (None, None)

            if u'사용권한이 없습니다' in msg:
                if not get_sign_on_status(request, page, soup):
                    return (self.ERROR_SIGNED_OUT, msg)
                else:
                    return (self.ERROR_GENERIC, msg)
            else:
                return (self.ERROR_GENERIC, msg)
        except:
            return (None, None)

parser_object = parser()
