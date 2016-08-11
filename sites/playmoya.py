import urllib
import re
import json


def searchfunction(searchterm):
    try:
        baseurl = "https://plamoya.com/index.php?main_page=advanced_search_result&search_in_description=0&"
        url = baseurl + urllib.urlencode({"keyword":searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('"centerBoxContentsProducts(.+?<div>.+?)</div>', info, flags=re.DOTALL)
        imageurl = "http://plamoya.com/" + re.findall('src="(.+?)"', figures[0])[0]
        imagename = re.findall('/.+/(.+)', imageurl)[0]
        f = open("html/images/" + imagename, 'wb')
        f.write(urllib.urlopen(imageurl).read())
        f.close
        stockurl = re.findall('href="(.+?)">', figures[0])[0]
        stockinfo = urllib.urlopen(stockurl).read()
        stock = re.findall('price.</div>.+?<div class=.+?>(.+?)<', stockinfo, flags=re.DOTALL)
        figure = {"title": re.findall('alt="(.+?)" t', figures[0])[0],
                  "price": re.findall('\$(.+)', figures[0])[0].replace(",", ""),
                  "stock": stock[0],
                  "image": imagename,
                  "source": "Playmoya",
                  "link": re.findall('href="(.+?)"', figures[0])[0]}
        exchangerate = json.loads(urllib.urlopen("http://api.fixer.io/latest?base=USD").read())
        figure["price"] = str(int(float(figure["price"]) * exchangerate["rates"]["JPY"]))
        return figure
    except:
        return {"title": "Figure not Found"}