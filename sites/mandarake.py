# -*- coding: utf-8 -*-
import urllib
import re


def searchfunction(searchterm):
    try:
        baseurl = "http://order.mandarake.co.jp/order/listPage/serchKeyWord?categoryCode=00&"
        url = baseurl + urllib.urlencode({"keyword":searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('<div class="basic".+?stock">(.+?)"category"', info, flags=re.DOTALL | re.UNICODE)
        imageurl = re.findall('src="(.+?)"', figures[0])[0]
        imagename = re.findall('/.+/(.+)', imageurl)[0]
        f = open("images/" + imagename, 'wb')
        f.write(urllib.urlopen(imageurl).read())
        f.close

        figure = {"title": re.findall('<p>.+?>(.+?)<', figures[0], flags=re.DOTALL | re.UNICODE)[0].strip(),
                  "price": re.findall('<div class="price">.+?>(.+?)円', figures[0], flags=re.DOTALL | re.UNICODE)[0].replace(",", ""),
                  "stock": re.findall('(.+?)<', figures[0], flags=re.DOTALL | re.UNICODE)[0],
                  "image": imagename,
                  "source": "Mandarake"}
        return figure
    except:
        return {"title": "Figure not Found"}