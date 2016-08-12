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
    <html lang="en">

    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- The above 3 meta tags *must* come first in the head; any other head
             content must come *after* these tags -->
        <title>"pagetitle"</title>
        <!-- Bootstrap -->
        <link href="css/bootstrap.min.css" rel="stylesheet">
        <link href="css/bootstrap-theme.min.css" rel="stylesheet">

        <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
        <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
        <![endif]-->
        <link href="main.css" rel="stylesheet">
    </head>
    '''
html = html.replace('"pagetitle"', search.title() + " Results")
html += '''
    <body>
        <header class="jumbotron">
            <div class="container text-center text-center">
                <div class="row row-header">
                    <div class="col-xs-12">
                        <h1>"search"</h1>
                    </div>
                </div>
            </div>
        </header>

        <div class="container text-center">
'''
html = html.replace('"search"', search.title())
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
    html += '''
            <div class="row text-center">
                <h1 class="text-center">"source"</h1>
            </div>
            <div class="row text-center">
                <div class="col-xs-12 col-sm-2 data well well-lg text-center">
                    <a href=""sitelink""><img src=""imagename"" class="img-responsive" /></a>
                </div>
                <div class="col-xs-12 col-sm-6 data well well-lg text-center">
                    "title"
                </div>
                <div class="col-xs-6 col-sm-2 data well well-lg text-center">
                    "price"
                </div>
                <div class="col-xs-6 col-sm-2 data well well-lg text-center">
                    "stock"
                </div>
            </div>
    '''
    html = html.replace('"source"', item[0])
    html = html.replace('"sitelink"', item[5])
    html = html.replace('"imagename"', "images/" + item[4].replace(" ", "%20"))
    html = html.replace('"title"', item[1])
    html = html.replace('"price"', item[2])
    html = html.replace('"stock"', item[3])
html += '''
        </div>

        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <!-- Include all compiled plugins (below), or include individual files as needed -->
        <script src="html/js/bootstrap.min.js"></script>
    </body>
</html>
'''
f = open("html/" + search + ".html", "wb")
f.write(html)
f.close
html2 = '''
<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- The above 3 meta tags *must* come first in the head; any other head
             content must come *after* these tags -->
        <title>Searches</title>
        <!-- Bootstrap -->
        <link href="html/css/bootstrap.min.css" rel="stylesheet">
        <link href="html/css/bootstrap-theme.min.css" rel="stylesheet">

        <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
        <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
        <![endif]-->
        <link href="html/main.css" rel="stylesheet">
    </head>

    <body>
        <div class="container">
            <div class="row">
'''
f2 = open("searches.html", "wb")
onlyfiles = [f for f in listdir("html/") if isfile(join("html/", f))]
for file in onlyfiles:
    if file != "main.css":
        html2 += '''
                    <div class="col-xs-12 col-sm-3">
                        <div class="well text-center"><a href=""searchlink""><h3>"search"</h3></a></div>
                    </div>
        '''
        html2 = html2.replace('"searchlink"', "html/" + file)
        html2 = html2.replace('"search"', file[:-5].title())
html2 += '''
            </div>
        </div>
        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <!-- Include all compiled plugins (below), or include individual files as needed -->
        <script src="js/bootstrap.min.js"></script>
    </body>
'''
f2.write(html2)
f2.close()
# conn.commit()
