import urllib
import re


def searchfunction(searchterm):
    try:
        baseurl = "http://slist.amiami.com/top/search/list?s_"
        url = baseurl + urllib.urlencode({"keywords":searchterm, "submit":"Search", "pagemax":"1"})
        info = urllib.urlopen(url).read()
        figures = re.findall('<td class="product_box">(.+?)</td>', info, flags=re.DOTALL)
        figure = {"title": re.findall('<.+?product_name_list">.+?>(.+?)<', figures[0])[0],
                  "price": re.findall('/span>\\n\\t\\t\\t\\t\\n\\t\\t\\t\\t(.+?) JPY', figures[0])[0].replace(",", ""),
                  "stock": re.findall('Stock</b>: (.+?) -->', figures[0])[0]}
        return figure
    except:
        return {"title": "Figure not Found"}