import urllib
import re


def searchfunction(searchterm):
        baseurl = "http://hlj.com/scripts/hljlist?GenreCode2=all&"
        url = baseurl + urllib.urlencode({"Word": searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('<table class="tbl-searchresults tblcss3">(.+?)<\/tr>', info, flags=re.DOTALL)
        figure = {"title": re.findall('f-itemname">\\n(.+?)\\n<', figures[0])[0].strip(),
                  "price": re.findall('&yen;(.+?) \\n<', figures[0])[0].replace(",", ""),
                  "stock": ""}
        try:
            figure["stock"] = re.findall('<span class="bold base-text.+?\\n(.+?)<span', figures[0])[0].replace("<br />", "")
        except:
            try:
                figure["stock"] = re.findall('<span class="bold base-text.+?\\n(.+?)\\n', figures[0])[0]
            except:
                figure["stock"] = "Couldn't determine stock"
        if "&nbsp" in figure["stock"]:
            figure["stock"] = re.findall('(.+?)<br>', figure["stock"])[0].replace("&nbsp;", " ")
        return figure