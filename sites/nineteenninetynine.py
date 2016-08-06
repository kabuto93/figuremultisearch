import urllib
import re


def searchfunction(searchterm):
    try:
        baseurl = "http://www.1999.co.jp/eng/search?typ1_c=101&cat=&state=&sold=0&sortid=0&"
        url = baseurl + urllib.urlencode({"searchkey": searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('<table id="masterBody_ilList_lvList_ctrl0_tblItemList_0" width="815">(.+?)Add to Wish List', info, flags=re.DOTALL)
        figure = {"title": re.findall('<span id="masterBody_ilList_lvList_ctrl0_lblItemName_0">(.+?)<\/span>', figures[0])[0],
                  "price": re.findall('font-weight: bold;">(.+?) yen', figures[0])[0].replace(",", ""),
                  "stock": "",
                  "source": "1999.co.jp"}
        try:
            re.findall('(Sold Out)', figures[0])[0]
            figure["stock"] = "Sold out"
        except:
            figure["stock"] = "In stock"
        return figure
    except:
        return {"title": "Figure not Found"}
