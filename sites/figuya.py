# -*- coding: utf-8 -*-
import urllib
import re
import json


def searchfunction(searchterm):
    try:
        baseurl = "https://figuya.com/de/produkte/search?"
        url = baseurl + urllib.urlencode({"q[query]":searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall("product-card(.+?)</small>", info, flags=re.DOTALL)
        imageurl = 'https://figuya.com' + re.findall('src="(.+?)"', figures[0])[0]
        imagename = re.findall('/.+/(.+)', imageurl)[0]
        f = open("images/" + imagename, 'wb')
        f.write(urllib.urlopen(imageurl).read())
        f.close
        figure = {"title": re.findall('a id=.+?">(.+?)<', figures[0])[0],
                  "price": re.findall('<b>(.+?)>', figures[0])[0].replace(",", ".")[:-6].strip(),
                  "stock": re.findall("span clas.+?>(.+?)<", figures[0])[0],
                  "image": imagename,
                  "source": "Figuya"}
        exchangerate = json.loads(urllib.urlopen("http://api.fixer.io/latest?base=EUR").read())
        figure["price"] = str(int(float(figure["price"]) * exchangerate["rates"]["JPY"]))
        return figure
    except:
        return {"title": "Figure not Found"}