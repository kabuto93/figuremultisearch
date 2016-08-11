import urllib2,cookielib,re,urllib


def searchfunction(searchterm):
    try:
        url = "https://www.nippon-yasan.com/search.php?orderby=position&orderway=desc&submit_search=Search&"
        site = url + urllib.urlencode({"search_query": searchterm})
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        req = urllib2.Request(site, headers=hdr)

        try:
            page = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()

        content = page.read()
        figures = re.findall('availability(.+?)</li>', content, flags=re.DOTALL)
        title = re.findall('title="(.+?)"', figures[0])[0]
        price = re.findall('price.+?>(.+?)<', figures[0])[0][:-2]
        imageurl = re.findall('src="(.+?)"', figures[0])[0]
        imagename = re.findall('.+?/.+/(.+)', imageurl)[0]
        stock = re.findall('.+?(\S.+?)\n', figures[0][2:])[0].strip()
        figure = {"title": title.strip(),
                  "price": price.replace(",", ""),
                  "stock": stock,
                  "image": imagename,
                  "source": "Nippon-Yassan",
                  "link": re.findall('href="(.+?)"', figures[0])[0]}
        req2 = urllib2.Request(imageurl, headers=hdr)

        try:
            page = urllib2.urlopen(req2)
        except urllib2.HTTPError, e:
            print e.fp.read()


        f = open("images/" + imagename, 'wb')
        f.write(page.read())
        f.close()
        return figure
    except:
        return {"title": "Figure not Found"}