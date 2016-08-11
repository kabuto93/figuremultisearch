import urllib
import re


def searchfunction(searchterm):
    try:
        baseurl = "http://biginjap.com/en/search?orderby=p.date_add&orderway=desc&submit_search=Search&n=1&"
        url = baseurl + urllib.urlencode({"search_query": searchterm})
        info = urllib.urlopen(url).read()
        figures = re.findall('div class="product-block(.+?)cart', info, flags=re.DOTALL)
        imageurl = re.findall('<img src="(.+?)"', figures[0])[0]
        imagename = re.findall('/.+/(.+)', imageurl)[0]
        f = open("images/" + imagename, 'wb')
        f.write(urllib.urlopen(imageurl).read())
        f.close
        figure = {"title": re.findall('title="(.+?)">', figures[0])[0].strip(),
                  "price": re.findall('display: inline;">(.+?)<', figures[0])[0].replace(" ", "")[:-2],
                  "stock": re.findall('ity">(.+?)<', figures[0])[0],
                  "image": imagename,
                  "source": "Big in Japan",
                  "link": re.findall('href="(.+?)"', figures[0])[0]}
        return figure
    except:
        return {"title": "Figure not Found"}