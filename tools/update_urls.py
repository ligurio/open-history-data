#!/usr/bin/env python2.7
#
# https://yandex.ru/support/site/themes/http-addtheme.xml
#

import re, sys, markdown, requests, bs4 as BeautifulSoup, httplib, urllib

reload(sys)
sys.setdefaultencoding('utf8')

# https://site.yandex.ru/themes/
key="94716cf81920311f3c45eaa58f53a85a240c147e"
category_id="4003560"
login_id="ligurio"

def retrieve_urls(filename):
    with open(filename) as fd:
        mdtext = fd.read()
        html_text = markdown.markdown(mdtext)
        soup = BeautifulSoup.BeautifulSoup(html_text, "html.parser")
        return [a['href'] for a in soup.findAll('a')]

def get_urls(filename):
    urls=""
    for url in retrieve_urls(filename):
        r = "(?:http[s]?://[^)]+)"
        u = re.findall(r, url)
        if not u: continue
        urls+=' '+u[0]
        print u[0]
    return urls

def post_urls(urls):
    params = urllib.urlencode({ 'key' : key, 'id' : login_id, 'category_id' : category_id, 'urls' : urls})
    headers = {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Accept'] = '*/*'
    conn = httplib.HTTPConnection("site.yandex.ru", 80)
    conn.set_debuglevel(1)
    conn.request("POST", "/update_urls.xml", params, headers)
    response = conn.getresponse()
    #print response.status, response.reason
    data = response.read()
    conn.close()

def main():
    urls=get_urls(sys.argv[1])
    post_urls(urls)

if __name__ == '__main__':
    main()
