from sites import amiami, biginjapan, crunchyroll, goodsmilecompany, hlj, kirinhobby, nineteenninetynine, playmoya, mandarake, animeblvd, nipponyassan, animefiguren, animeisland, animegami, bigbadtoystore, figuya, ixudeviance
import urllib
import json
import sqlite3
from threading import Thread
import httplib, sys
from Queue import Queue
from os import listdir
from os.path import isfile, join


global search
global figurelist
concurrent = 200
figurelist = []
q = Queue(concurrent * 2)


def doWork():
    global search
    while True:
        url = q.get()
        figure = url.searchfunction(search)
        doSomethingWithResult(figure)
        q.task_done()


def doSomethingWithResult(figure):
    global html
    if figure["title"] == "Figure not Found":
        pass
    else:
        figurelist.append(figure)


fh = open("config.txt")
settings = []
for line in fh:
    try:
        settings.append(line.split("=")[1].strip())
    except:
        break
fh.close()
basecur = "JPY"
targetcur = settings[0]
search = raw_input()
global html
html = '''
    <!DOCTYPE html>
    <html>
    <head lang="en">
        <title>"pagetitle"</title>
        <meta charset="UTF-8">
        <meta name="description" content="Search results">
        <meta name="author" content="Steven Rexroth">
        <link rel="stylesheet" type="text/css" href="main.css">
    </head>
    <body>
    '''
html = html.replace('"pagetitle"', search + " results")
html += '''
<h1>"search"</h1>
'''
html = html.replace('"search"', search)
# conn = sqlite3.connect('figuredb.sqlite')
# cur = conn.cursor()
# cur.execute('''CREATE TABLE IF NOT EXISTS Figures (search TEXT, source TEXT, title TEXT, price TEXT, stock TEXT,image TEXT, PRIMARY KEY(search, source))''')

sitesdict = {"amiami": amiami, "biginjapan": biginjapan, "crunchyroll": crunchyroll, "goodsmilecompany": goodsmilecompany,"hlj": hlj, "kirinhobby": kirinhobby, "nineteenninetynine": nineteenninetynine, "playmoya": playmoya, "mandarake": mandarake, "animeblvd": animeblvd, "nipponyassan": nipponyassan, "animefiguren": animefiguren, "animeisland": animeisland, "animegami": animegami, "bigbadtoystore": bigbadtoystore, "figuya": figuya, "ixudeviance": ixudeviance}
sites = settings[1].split(",")
usersites = []
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
for item in sites:
    usersites.append(sitesdict[item])
results = []
exchangerate = json.loads(urllib.urlopen("http://api.fixer.io/latest?base=" + basecur.upper()).read())
try:
    for item in usersites:
        q.put(item)
    q.join()
except KeyboardInterrupt:
    sys.exit(1)
for item in figurelist:
    item["price"] = str(round(float(item["price"]) * exchangerate["rates"][targetcur.upper()], 2))
    results.append([item["source"], item["title"], item["price"], item["stock"], item["image"], item["link"]])
for item in results:
    print "Site: " + item[0] + " | Item: " + item[1] + " | Price: " + item[2] + targetcur + " | Status: " + item[3]
#     cur.execute('''INSERT OR IGNORE INTO Figures (search, source, title, price, stock, image) VALUES ( ?, ?, ?, ?, ?, ? )''', (buffer(search), buffer(item[0]), buffer(item[1]), buffer(item[2]), buffer(item[3]), buffer(item[4])))
#     cur.execute('''UPDATE Figures SET title = ?, price = ?, stock = ?, image = ? WHERE search = ? AND source = ?''', (buffer(item[1]), buffer(item[2]), buffer(item[3]), buffer(item[4]), buffer(search), buffer(item[0])))
    html += '<fieldset><legend>"source"</legend><table><tr><td id="img"><label><a href=""sitelink""><img src=""image name"" /></a></label></td><td id="big"><label>"title"</label></td><td><label>"price"</label></td><td><label>"stock"</label></td></tr></table></fieldset>'
    html = html.replace('"source"', item[0])
    html = html.replace('"sitelink"', item[5])
    html = html.replace('"image name"', "images/" + item[4].replace(" ", "%20"))
    html = html.replace('"title"', item[1])
    html = html.replace('"price"', item[2])
    html = html.replace('"stock"', item[3])
f = open("html/" + search + ".html", "wb")
f.write(html)
f.close
html2 = ""
f2 = open("searches.html", "wb")
onlyfiles = [f for f in listdir("html/") if isfile(join("html/", f))]
for file in onlyfiles:
    if file != "main.css":
        html2 += '<a href="html/' + file + '">' + file[:-5] + '</a><br />'
f2.write(html2)
f2.close()
# conn.commit()
