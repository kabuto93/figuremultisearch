import urllib
import re


def searchfunction(searchterm):
    try:
        baseurl = "http://goodsmileshop.com/en/search/?"
        url = baseurl + urllib.urlencode({"text":searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('productGridI.+?>(.+?)productG', info, flags=re.DOTALL)
        imageurl = "http://goodsmileshop.com/" + re.findall('src="(.+?)"', figures[0])[0]
        imagename = "goodsmile" + searchterm + ".jpg"
        f = open("images/" + imagename, 'wb')
        f.write(urllib.urlopen(imageurl).read())
        f.close
        figure = {"title": re.findall('3>(.+?)<', figures[0])[0],
                  "price": re.findall('price.+?> ..(.+?)<', figures[0])[0].replace(",", ""),
                  "stock": re.findall('<li.+?>\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.+?)<', figures[0])[0],
                  "image": imagename,
                  "source": "Good Smile Company"}
        return figure
    except:
        return {"title": "Figure not Found"}

searchfunction("love live")