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

        pages = soup.findAll('td', {'align': 'center', 'colspan': '2', 'nowrap': 'nowrap'})[0]

        for pagelink in pages.findAll('a'):
            if pagelink.text == u'[계속 검색]':
                output['divnext'] = int(divpage_matcher.match(find_attr(pagelink, 'href')).group(1))
            elif pagelink.text == u'[이전 검색]':
                output['divprev'] = int(divpage_matcher.match(find_attr(pagelink, 'href')).group(1))

        maxpages = 1
        for page in pages.findAll('font'):
            try:
                pnum = int(decimal_matcher.match(page.text).group(1))
                if pnum > maxpages:
                    maxpages = pnum
            except Exception, e:
                pass
        output['maxpages'] = maxpages
        
        trs = soup.findAll('tr', {'align': 'center', 'onmouseover': 'this.style.backgroundColor=\'#F5F5F5\''})

        cnt = 1
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
                link = '/view/%s/%s' % (pid, no_matcher.match(find_attr(tags.contents[6].contents[5], 'href')).group(1))
            except:
                link = '#'

            nitem = {'name': title, 'author': author, 'comment': comments, 'link': link}
            if zbllist.has_key(cnt):
                nitem.update(zbllist[cnt])

            alist.append(nitem)
            cnt += 1
        
        return output

    def parse_view(self, pid, page, soup):
        output = {}

        if 'memo_on.swf' in page:
            output['new_privmsg'] = True

        headers = soup.find('table', {'bgcolor': '#EFEFEF'}).findAll('tr')
        for n in headers:
            if 'Name' in n.contents[1].text:
                output['name'] = n.contents[3].contents[0].contents[0].text
                output['userid'] = n.contents[3].contents[0].contents[1].strip()[1:-1]
            elif 'Home' in n.contents[1].text:
                output['homepage'] = n.contents[3].text
            elif 'Subject' in n.contents[1].text:
                output['subject'] = n.contents[3].text

        if len(soup.findAll('form')) == 0:
            output['nocomments'] = True
        
        body = soup.find('span', {'style': 'line-height:160%'})
        body.find('div').replaceWith('')
        output['body'] = body.renderContents()

        comments = []
        cmtnodes = soup.findAll('table', {'border': '0', 'cellspacing': '0', 'cellpadding': '0', 'width': '95%'})[4].findAll('tr', {'align': 'center'})
        for n in cmtnodes:
            cmtnode = {}
            try:
                cmtnode['name'] = postprocess_string(n.contents[1].contents[0].text)
                cmtnode['body'] = postprocess_string(n.contents[7].renderContents())
                date = map(lambda x: x[:-1], n.contents[3].contents[0].contents[1].attrs[0][1].split())
                cmtnode['date'] = '%s/%s %s:%s:%s' % (date[1], date[2], date[3], date[4], date[5])

                try:
                    cmtnode['did'] = cno_matcher.match(filter(lambda x: x[0] == 'href', n.contents[9].contents[0].attrs)[0][1]).group(1)
                except:
                    pass

                comments.append(cmtnode)
            except:
                break

        output['comments'] = comments

        if len(soup.findAll('input', {'type': 'text'})) == 0:
            output['nocomments'] = True
        if soup.find('a', text='[Write]') and soup.find('a', text='[Modify]'):
            output['modify'] = True

        return output

    def check_write(self, pid, page, soup):
        output = {}

        try:
            output['subject'] = filter(lambda x: x[0] == 'value', soup.find('input', {'type': 'text', 'name': 'subject'}).attrs)[0][1]
            output['contents'] = soup.find('textarea', {'name': 'memo'}).text
        except:
            pass

        categories = []
        nodes = soup.find('select', {'name': 'category'})
        
        for i in nodes.findAll('option')[1:]:
            cat = {'value': i.attrs[0][1], 'name': postprocess_string(i.text)}
            if len(filter(lambda x: x[0] == 'selected', i.attrs)) > 0:
                cat['selected'] = True
            categories.append(cat)
        
        if len(categories) > 0:
            output['categories'] = categories
        
        return output

    def check_error(self, request, page, soup):
        try:
            error = find_common_error(page, soup)
            if error:
                return error

            msg = soup.find('td').find('font', {'color': 'red'}).find('b').text.strip()
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
