import urllib
import re
import json


def searchfunction(searchterm):
    try:
        baseurl = "https://animegami.co.uk/shop/page/1/?products_per_page=1&"
        url = baseurl + urllib.urlencode({"s":searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('product type(.+?)<\/li>', info, flags=re.DOTALL)
        imageurl = re.findall('src="(.+?)"', figures[0])[0]
        imagename = re.findall('/.+/(.+)', imageurl)[0]
        f = open("images/" + imagename, 'wb')
        f.write(urllib.urlopen(imageurl).read())
        f.close
        figure = {"title": re.findall('a href=.+title="(.+?)>', figures[0])[0],
                  "price": re.findall('</span>(.+?)<', figures[0])[0].replace(",", ""),
                  "stock": re.findall('span.+<span.+class.+?>(.+?)<', figures[0], flags=re.DOTALL)[0],
                  "image": imagename,
                  "source": "Animegami"}
        exchangerate = json.loads(urllib.urlopen("http://api.fixer.io/latest?base=USD").read())
        figure["price"] = str(int(float(figure["price"]) * exchangerate["rates"]["JPY"]))
        return figure
    except:
        return {"title": "Figure not Found"}

print searchfunction("no game no life rage of bahamut")