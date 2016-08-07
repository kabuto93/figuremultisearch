from sites import amiami, biginjapan, crunchyroll, goodsmilecompany, hlj, kirinhobby, nineteenninetynine, playmoya
import urllib
import json


basecur = "JPY"
targetcur = "USD"
search = "love live figure"

sites = [amiami, biginjapan, crunchyroll, goodsmilecompany, hlj, kirinhobby, nineteenninetynine, playmoya]
results = []
exchangerate = json.loads(urllib.urlopen("http://api.fixer.io/latest?base=" + basecur.upper()).read())
for item in sites:
    working = item.searchfunction(search)
    if working["title"] == "Figure not Found":
        continue
    working["price"] = str(round(float(working["price"]) * exchangerate["rates"][targetcur.upper()], 2))
    results.append([working["source"], working["title"], working["price"], working["stock"]])
for item in results:
    print "Site: " + item[0] + " | Item: " + item[1] + " | Price: " + item[2] + targetcur + " | Status: " + item[3]