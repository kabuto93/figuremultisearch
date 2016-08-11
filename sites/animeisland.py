import urllib
import re
import json


def searchfunction(searchterm):
    try:
        baseurl = "http://www.anime-island.com/search.php?x=0&y=0&"
        url = baseurl + urllib.urlencode({"search_query":searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('<li class="Even">(.+?)<li', info, flags=re.DOTALL)
        imageurl = re.findall('src="(.+?)\?', figures[0])[0]
        imagename = re.findall('/.+/(.+)', imageurl)[0]
        f = open("images/" + imagename, 'wb')
        f.write(urllib.urlopen(imageurl).read())
        f.close
        price = re.findall('Rating">.+em(.+)/em', figures[0], flags=re.DOTALL)[0].strip()
        try:
            price = re.findall('e>(.+?)<', price)[0].strip()[1:]
        except:
            price = price[1:]
        figure = {"title": re.findall('alt="(.+?)"', figures[0])[0],
                  "price": price,
                  "stock": "Stock info is not available from this source",
                  "image": imagename,
                  "source": "Anime Island",
                  "link": re.findall('href="(.+?)"', figures[0])[0]}
        exchangerate = json.loads(urllib.urlopen("http://api.fixer.io/latest?base=USD").read())
        figure["price"] = str(int(float(figure["price"]) * exchangerate["rates"]["JPY"]))
        return figure
    except:
        return {"title": "Figure not Found"}