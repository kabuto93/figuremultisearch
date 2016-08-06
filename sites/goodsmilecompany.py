import urllib
import re


def searchfunction(searchterm):
    try:
        baseurl = "http://goodsmileshop.com/en/search/?"
        url = baseurl + urllib.urlencode({"text":searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('productGridI.+?>(.+?)productG', info, flags=re.DOTALL)
        figure = {"title": re.findall('3>(.+?)<', figures[0])[0],
                  "price": re.findall('price.+?> ..(.+?)<', figures[0])[0].replace(",", ""),
                  "stock": re.findall('<li.+?>\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.+?)<', figures[0])[0],
                  "source": "Good Smile Company"}
        return figure
    except:
        return {"title": "Figure not Found"}