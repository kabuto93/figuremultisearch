import urllib
import re
import json


def searchfunction(searchterm):
    try:
        baseurl = "http://www.bigbadtoystore.com/bbts/search.aspx?"
        url = baseurl + urllib.urlencode({"search":searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('<FONT size="3">(.+?)width="180"', info, flags=re.DOTALL)
        imageurl = 'http://www.bigbadtoystore.com' + re.findall('img src="(.+?)"', figures[0])[0]
        imagename = re.findall('/.+/(.+)', imageurl)[0]
        f = open("images/" + imagename, 'wb')
        f.write(urllib.urlopen(imageurl).read())
        f.close
        figure = {"title": re.findall('<b>(.+?)</b>', figures[0], flags=re.DOTALL)[0].strip(),
                  "price": re.findall('lblPrice">\$(.+?)<', figures[0])[0].replace(",", ""),
                  "stock": re.findall('lblStatus">.+?>(.+?)<', figures[0])[0],
                  "image": imagename,
                  "source": "Big Bad Toy Store"}
        exchangerate = json.loads(urllib.urlopen("http://api.fixer.io/latest?base=USD").read())
        figure["price"] = str(int(float(figure["price"]) * exchangerate["rates"]["JPY"]))
        return figure
    except:
        return {"title": "Figure not Found"}