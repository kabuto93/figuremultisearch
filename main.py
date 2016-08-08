from sites import amiami, biginjapan, crunchyroll, goodsmilecompany, hlj, kirinhobby, nineteenninetynine, playmoya
import urllib
import json
import sqlite3


basecur = "JPY"
targetcur = "USD"
search = raw_input()
html = '''
    <!DOCTYPE html>
    <html>
    <head lang="en">
        <title>Matching Game</title>
        <meta charset="UTF-8">
        <meta name="description" content="Find the odd one out.">
        <meta name="author" content="Steven Rexroth">
        <link rel="stylesheet" type="text/css" href="main.css">
    </head>
    <body>
    '''
html += '''
<h1>"search"</h1>
'''
html = html.replace('"search"', search)
conn = sqlite3.connect('figuredb.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Figures (search TEXT, source TEXT, title TEXT, price TEXT, stock TEXT,image TEXT, PRIMARY KEY(search, source))''')


sites = [amiami, biginjapan, crunchyroll, goodsmilecompany, hlj, kirinhobby, nineteenninetynine, playmoya]
results = []
exchangerate = json.loads(urllib.urlopen("http://api.fixer.io/latest?base=" + basecur.upper()).read())
for item in sites:
    working = item.searchfunction(search)
    if working["title"] == "Figure not Found":
        continue
    working["price"] = str(round(float(working["price"]) * exchangerate["rates"][targetcur.upper()], 2))
    results.append([working["source"], working["title"], working["price"], working["stock"], working["image"]])
for item in results:
    print "Site: " + item[0] + " | Item: " + item[1] + " | Price: " + item[2] + targetcur + " | Status: " + item[3]
    cur.execute('''INSERT OR IGNORE INTO Figures (search, source, title, price, stock, image) VALUES ( ?, ?, ?, ?, ?, ? )''', (buffer(search), buffer(item[0]), buffer(item[1]), buffer(item[2]), buffer(item[3]), buffer(item[4])))
    cur.execute('''UPDATE Figures SET title = ?, price = ?, stock = ?, image = ? WHERE search = ? AND source = ?''', (buffer(item[1]), buffer(item[2]), buffer(item[3]), buffer(item[4]), buffer(search), buffer(item[0])))
    html += '<fieldset><legend>"source"</legend><table><tr><td id="img"><label><img src="image name" /></label></td><td id="big"><label>"title"</label></td><td><label>"price"</label></td><td><label>"stock"</label></td></tr></table></fieldset>'
    html = html.replace('"source"', item[0])
    html = html.replace('"image name"', "images/" + item[4].replace(" ", "%20"))
    html = html.replace('"title"', item[1])
    html = html.replace('"price"', item[2])
    html = html.replace('"stock"', item[3])
f = open(search + ".html", "wb")
f.write(html)
f.close
conn.commit()
