# -*- coding: utf-8 -*-
import urllib
import re
import json


def searchfunction(searchterm):
    try:
        baseurl = "https://anime-figuren.de/index.php?lang=0&cl=search&"
        url = baseurl + urllib.urlencode({"searchparam":searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('pictureBox(.+?)\*', info, flags=re.DOTALL)
        imageurl = re.findall('src="(.+?)"', figures[0])
        imagename = re.findall('/.+/(.+)', imageurl[0])[0]
        f = open("images/" + imagename, 'wb')
        f.write(urllib.urlopen(imageurl[0]).read())
        f.close
        price = re.findall(r'"price">.+?\b.+?>.+?\b.+?>(.+)', figures[0], flags=re.DOTALL)[0].strip()[:-3].replace(",", ".")
        figure = {"title": re.findall('alt="(.+?)"', figures[0])[0],
                  "price": price,
                  "stock": 'Stock info not available',
                  "image": imagename,
                  "source": "Anime Figuren"}
        exchangerate = json.loads(urllib.urlopen("http://api.fixer.io/latest?base=EUR").read())
        figure["price"] = str(int(float(figure["price"]) * exchangerate["rates"]["JPY"]))
        return figure
    except:
        return {"title": "Figure not Found"}