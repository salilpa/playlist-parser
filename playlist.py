from flask import Flask, request
from functions import *
import json
from decorator import crossdomain
from settings import db, PER_PAGE
from pagination import Pagination

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
    station = db.stations.find_one({"name": name})
    if station:
        keywords = video_text_from_url(station["url"], station["settings"], station["soup_path_for_list"], station["soup_path_for_keyword"])
        videos = []
        for keyword in keywords:
            videos.append(get_video_from_keyword(keyword))
        return "total number of videos is " + str(len(videos))
    #get the radio station from the object
    #get keywords from the object parameter
    else:
        return "Incomplete function"

@app.route('/<string:meta_key>/<string:meta_val>/page/<int:page_number>')
def get_meta_value(meta_key, meta_val, page_number):
    stations = db.stations.find({"meta." + meta_key: meta_val})
    count = stations.count()
    if count > (page_number - 1)*PER_PAGE:
        #should return list of objects divided by page
        stations_to_be_displayed = stations[(page_number-1)*PER_PAGE:page_number*PER_PAGE]
        pagination = Pagination(page_number, PER_PAGE, count)
        return "More than zero documents"
    else:
        return "None found"

@app.route('/<string:meta_key>/page/<int:page_number>')
def get_meta_key(meta_key, page_number):
    stations = db.stations.distinct("meta." + meta_key)
    count = len(stations)
    if count > (page_number - 1)*PER_PAGE:
        #should return list of objects divided by page
        stations_to_be_displayed = stations[(page_number-1)*PER_PAGE:page_number*PER_PAGE]
        pagination = Pagination(page_number, PER_PAGE, count)
        return "More than zero documents"
    else:
        return "None found"

@app.route('/')
def index():
    #find all meta keys and give urls to it
    return "dummy index function"