import urllib
import re
import json


def searchfunction(searchterm):
    try:
        baseurl = "http://www.crunchyroll.com/search?from=store&"
        url = baseurl + urllib.urlencode({"q":searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('product-thumb(.+?)</s', info, flags=re.DOTALL)
        imageurl = re.findall('src="(.+?)"', figures[0])[0]
        imagename = re.findall('/.+/(.+)', imageurl)[0]
        f = open("images/" + imagename, 'wb')
        f.write(urllib.urlopen(imageurl).read())
        f.close
        figure = {"title": re.findall('alt="(.+?)"/>', figures[0])[0],
                  "price": re.findall('ce">\n.+\$(.+)', figures[0])[0].replace(",", ""),
                  "stock": "CR doesn't give stock info",
                  "image": imagename,
                  "source": "Crunchyroll"}
        exchangerate = json.loads(urllib.urlopen("http://api.fixer.io/latest?base=USD").read())
        figure["price"] = str(int(float(figure["price"]) * exchangerate["rates"]["JPY"]))
        return figure
    except:
        return {"title": "Figure not Found"}

searchfunction("love live")