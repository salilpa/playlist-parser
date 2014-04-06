from flask import Flask, request, render_template
from functions import *
import json
from decorator import crossdomain
from settings import db, PER_PAGE
from pagination import Pagination
from flask_functions import *
from flask_bootstrap import Bootstrap
from flask_frozen import Freezer

app = Flask(__name__)
app.config.from_pyfile('app_config.py')
Bootstrap(app)
freezer = Freezer(app)


#returns a page with links to all websites
'''
@app.route('/pageToKeywords/', methods=["POST", "GET", "OPTIONS"])
@crossdomain(origin='*')
def page_to_keywords():
    if request.method == 'POST':
        station = json.loads(request.data)
        return "|".join(video_text_from_url(station["url"], station["settings"], station["soup_path_for_list"],
                                            station["soup_path_for_keyword"]))
    else:
        return "All is well"
'''


@app.route('/station/<string:name>/')
def station_details(name):
    station = db.stations.find_one({"name": name})
    if station:
        keywords = video_text_from_url(station["url"], station["settings"], station["soup_path_for_list"],
                                       station["soup_path_for_keyword"])
        videos = []
        for keyword in keywords:
            videos.append(get_video_from_keyword(keyword))
        return render_template("station.html", videos=videos)
    #get the radio station from the object
    #get keywords from the object parameter
    else:
        return "Incomplete function"


@app.route('/<string:meta_key>/<string:meta_val>/page/<int:page_number>/')
def get_meta_value(meta_key, meta_val, page_number):
    stations = db.stations.find({"meta." + meta_key: meta_val})
    count = stations.count()
    if count > (page_number - 1) * PER_PAGE:
        #should return list of objects divided by page
        stations_to_be_displayed = stations[(page_number-1)*PER_PAGE:page_number*PER_PAGE]
        station_urls = create_url_objects_from_stations(stations_to_be_displayed)
        pagination = Pagination(page_number, PER_PAGE, count)
        return render_template("station_list.html", pagination=pagination, stations=station_urls)
    else:
        return "None found"


@app.route('/<string:meta_key>/page/<int:page_number>/')
def get_meta_key(meta_key, page_number):
    meta_values = generate_meta_key_urls(db, meta_key, page_number * PER_PAGE)
    count = len(meta_values)
    if count > (page_number - 1) * PER_PAGE:
        #should return list of objects divided by page
        meta_to_be_displayed = {
            "name": meta_key,
            "urls": meta_values[(page_number - 1) * PER_PAGE:page_number * PER_PAGE]
        }
        pagination = Pagination(page_number, PER_PAGE, count)
        return render_template("meta_list.html", pagination=pagination, meta_to_be_displayed=meta_to_be_displayed)
    else:
        return "None found"


@app.route('/')
def index():
    url_blocks = []
    url_blocks.append({
        "name": "country",
        "url": url_for(".get_meta_key", meta_key="country", page_number=1),
        "sub_urls": generate_meta_key_urls(db, "country", 3)
    })
    url_blocks.append({
        "name": "language",
        "url": url_for(".get_meta_key", meta_key="language", page_number=1),
        "sub_urls": generate_meta_key_urls(db, "language", 3)
    })
    #find all meta keys and give urls to it
    return render_template("index.html", url_blocks=url_blocks)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page
