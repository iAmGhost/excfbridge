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
        
        zbllist = {}
        for i in soup.findAll('script'):
            zbllist.update(parse_layer_info(i.text))

        if 'memo_on.swf' in page:
            output['new_privmsg'] = True

        # pages
        pager = soup.find('div', {'class': 'navbar_center'})
        prev_div = pager.find('a', {'class': 'prev_div'})
        next_div = pager.find('a', {'class': 'next_div'})

        if prev_div:
            output['divprev'] = int(divpage_matcher.match(prev_div['href']).group(1))
        if next_div:
            output['divnext'] = int(divpage_matcher.match(next_div['href']).group(1))
        nre = re.compile('^[0-9]+$')
        try:
            maxpages = int(filter(lambda x: nre.match(x), map(lambda y: y.renderContents(), pager.findAll('a')))[-1])
        except:
            maxpages = 1

        output['maxpages'] = maxpages

        # posts
        alist = soup.find('table').findAll('tr')
        posts = []
        cnt = 2
        for i in alist:
            sc = i.find('td', {'class': 'col_subject'})
            sn = i.find('td', {'class': 'col_name'})

            try:
                comments = sc.contents[1].find('span', {'class': 'comments'}).renderContents()
                sc.contents[1].find('span', {'class': 'comments'}).replaceWith('')
            except:
                comments = None
            
            try:
                title = sc.contents[1].renderContents()
                author = sn.contents[0].renderContents()
            except:
                continue

            try:
                link = '/view/%s/%s' % (pid, no_matcher.match(sc.contents[1]['href']).group(1))
            except:
                link = '#'

            notice = False

            it = {'name': title, 'author': author, 'comment': comments, 'link': link, 'sticky': notice}
            if zbllist.has_key(cnt):
                it.update(zbllist[cnt])

            posts.append(it)

            cnt += 1

        output['article_lists'] = posts

        return output

    def parse_view(self, pid, page, soup):
        output = {}

        zbllist = {}
        for i in soup.findAll('script'):
            zbllist.update(parse_layer_info(i.text))

        if 'memo_on.swf' in page:
            output['new_privmsg'] = True

        header = soup.find('ul', {'class': 'header'})
        for i in header.findAll('li'):
            title = i.find('span', {'class': 'title'}).text
            val = i.find('span', {'class': 'item'})

            if title == u'시각':
                output['date'] = val.text
            elif title == u'홈페이지':
                output['homepage'] = val.text
            elif title == u'제목':
                output['subject'] = val.text
            elif title == u'작성자':
                output['name'] = val.contents[0].text
                output['userid'] = val.contents[2].text
            
        output['body'] = '<br />' + soup.find('div', {'class': 'contents'}).renderContents()

        if zbllist.has_key(3):
            output.update(zbllist[3])

        comments = []
        cnt = 4
        for i in soup.find('table', {'id': 'comments'}).findAll('tr'):
            cmtnode = {}
            try:
                cmtnode['did'] = cno_matcher.match(i.find('span', {'class': 'delete'}).contents[0]['href']).group(1)
                i.contents[3].find('span').replaceWith('')
            except:
                pass
            cmtnode['name'] = i.contents[1].contents[0].text
            cmtnode['id'] = i.contents[1].contents[2].text
            cmtnode['body'] = i.contents[3].text
            cmtnode['date'] = i.contents[5].text

            if zbllist.has_key(cnt):
                cmtnode.update(zbllist[cnt])

            comments.append(cmtnode)
            cnt += 1

        output['comments'] = comments

        if soup.find('a', text=u'수정'):
            output['modify'] = True
        if len(soup.findAll('input', {'type': 'text'})) == 0:
            output['nocomments'] = True

        return output

    def check_write(self, pid, page, soup):
        output = {}

        try:
            output['subject'] = soup.find('input', {'type': 'text', 'name': 'subject'})['value']
            output['contents'] = soup.find('textarea', {'name': 'memo'}).text
        except:
            pass

        return output

    def check_error(self, request, page, soup):
        try:
            error = find_common_error(page, soup)
            if error:
                return error

            msg = soup.find('div', {'class': 'error'}).contents[1].text

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
