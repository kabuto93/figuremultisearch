import urllib2,cookielib,re,urllib,json


def searchfunction(searchterm):
    try:
        url = "https://www.animeblvd.com/catalogsearch/result/?cat=&"
        site = url + urllib.urlencode({"q": searchterm})
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
        figures = re.findall('loader m(.+?)actions', content, flags=re.DOTALL)
        title = re.findall('title="(.+?)"', figures[0])
        price = re.findall('\$(.+?)<', figures[0])
        imageurl = re.findall('src="(.+?)"', figures[0])[0]
        imagename = re.findall('.+?/.+/(.+)', imageurl)[0]
        stock = re.findall('div class="price-box"><span class=.+?>(.+?)<', figures[0])
        figure = {"title": title[0].strip(),
                  "price": price[0].replace(",", ""),
                  "stock": stock[0],
                  "image": imagename,
                  "source": "Anime Boulevard",
                  "link": re.findall('href="(.+?)"', figures[0])[0]}
        req2 = urllib2.Request(imageurl, headers=hdr)

        try:
            page = urllib2.urlopen(req2)
        except urllib2.HTTPError, e:
            print e.fp.read()


        f = open("images/" + imagename, 'wb')
        f.write(page.read())
        f.close()
        exchangerate = json.loads(urllib.urlopen("http://api.fixer.io/latest?base=USD").read())
        figure["price"] = str(int(float(figure["price"]) * exchangerate["rates"]["JPY"]))
        return figure
    except:
        return {"title": "Figure not Found"}