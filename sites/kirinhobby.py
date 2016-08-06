import urllib
import re
import json


def searchfunction(searchterm):
    try:
        baseurl = "http://www.kirinhobby.com/shop/advanced_search_result.php?"
        url = baseurl + urllib.urlencode({"keywords":searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('Listing-d(.+?)width="60"', info, flags=re.DOTALL)
        figure = {"title": re.findall('alt="(.+?)" t', figures[0])[0],
                  "price": re.findall('right".+?;\$(.+?)&', figures[0])[0].replace(",", ""),
                  "stock": re.findall('icon.+?><br />(.+?)<', figures[0])[0],
                  "source": "Kirin Hobby"}
        exchangerate = json.loads(urllib.urlopen("http://api.fixer.io/latest?base=USD").read())
        figure["price"] = str(int(float(figure["price"]) * exchangerate["rates"]["JPY"]))
        return figure
    except:
        return {"title": "Figure not Found"}