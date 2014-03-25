from flask import Flask, request
from functions import *
import json
from decorator import crossdomain
from settings import db

app = Flask(__name__)


#returns a page with links to all websites
@app.route('/pageToKeywords/', methods=["POST", "GET", "OPTIONS"])
@crossdomain(origin='*')
def page_to_keywords():
    if request.method == 'POST':
        station = json.loads(request.data)
        return "|".join(video_text_from_url(station["url"], station["settings"], station["soup_path_for_list"], station["soup_path_for_keyword"]))
    else:
        return "All is well"

@app.route('/station/<string:name>')
def station_details(name):
    station = db.stations.find({"name": name})
    #get the radio station from the object
    #get keywords from the object parameter
    return "Incomplete function"