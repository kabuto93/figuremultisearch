import urllib
import re


def searchfunction(searchterm):
    try:
        baseurl = "http://hlj.com/scripts/hljlist?GenreCode2=all&"
        url = baseurl + urllib.urlencode({"Word": searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('<table class="tbl-searchresults tblcss3">(.+?)<\/tr>', info, flags=re.DOTALL)
        imageurl = re.findall('img style="background-image: url\(\\\'\/\/(.+?)\'', figures[0])[0]
        imagename = re.findall('brc/(.+?)\?', imageurl)[0]
        f = open("images/" + imagename, 'wb')
        f.write(urllib.urlopen("http://" + imageurl).read())
        f.close
        figure = {"title": re.findall('f-itemname">\\n(.+?)\\n<', figures[0])[0].strip(),
                  "price": re.findall('&yen;(.+?) \\n<', figures[0])[0].replace(",", ""),
                  "stock": "",
                  "image": imagename,
                  "source": "HobbyLink Japan"}
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
    except:
        return {"title": "Figure not Found"}