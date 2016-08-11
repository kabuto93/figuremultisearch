import urllib
import re
import json


def searchfunction(searchterm):
    try:
        baseurl = "https://www.ixudeviance.com/fr/recherche?controller=search&orderby=position&orderway=desc&submit_search=Rechercher&"
        url = baseurl + urllib.urlencode({"search_query":searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('product-(.+?<span class="a.+?</span>)', info, flags=re.DOTALL)
        imageurl = re.findall('img src="(.+?)"', figures[0])[0]
        imagename = re.findall('/.+/(.+)', imageurl)[0]
        f = open("images/" + imagename, 'wb')
        f.write(urllib.urlopen(imageurl).read())
        f.close
        figure = {"title": re.findall('title="(.+?)"', figures[0])[0],
                  "price": re.findall('inline;">(.+?)<', figures[0])[0].replace(",", ".")[:-3].strip(),
                  "stock": re.findall('ability">(.+?)<', figures[0])[0],
                  "image": imagename,
                  "source": "iXu Deviance",
                  "link": re.findall('href="(.+?)"', figures[0])[0]}
        exchangerate = json.loads(urllib.urlopen("http://api.fixer.io/latest?base=EUR").read())
        figure["price"] = str(int(float(figure["price"]) * exchangerate["rates"]["JPY"]))
        return figure
    except:
        return {"title": "Figure not Found"}