from flask import Flask, render_template
from functions import *
from settings import db, PER_PAGE
from pagination import Pagination
from flask_functions import *
from flask_bootstrap import Bootstrap
from flask_frozen import Freezer

app = Flask(__name__)
app.config.from_pyfile('app_config.py')
Bootstrap(app)
freezer = Freezer(app)


@app.route('/')
def index():
    seo = {
        "title": "watch youtube videos of music charts automatically",
        "keywords": "music, charts, billboard, youtube, video, hot 100",
        "description": "watch the top music videos trending on music charts automatically"
    }
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
    breadcrumbs = [
        {
            "name": "home",
            "link": url_for(".index")
        }
    ]
    #find all meta keys and give urls to it
    return render_template("index.html", url_blocks=url_blocks, seo=seo, breadcrumbs=breadcrumbs)


@app.route('/<string:meta_key>/page/<int:page_number>/')
def get_meta_key(meta_key, page_number):
    seo = {
        "title": "watch youtube videos of music charts available in " + meta_key + " page " + str(page_number),
        "keywords": "music, charts, billboard, youtube, video, hot 100, page " + str(page_number) + ", " + meta_key,
        "description": "watch the top music videos trending on music charts automatically."
                       "track the top music charts available in your " + meta_key + " page " + str(page_number)
    }
    meta_values = generate_meta_key_urls(db, meta_key, PER_PAGE, (page_number-1) * PER_PAGE)
    #meta_values.sort(key=lambda x: x["count"], reverse=True)
    count = len(meta_values)
    if count > 0:
        #should return list of objects divided by page
        meta_to_be_displayed = {
            "name": meta_key,
            "urls": meta_values
        }
        pagination = Pagination(page_number, PER_PAGE, count)
        breadcrumbs = [
            {
                "name": "home",
                "link": url_for(".index")
            },
            {
                "name": meta_key,
                "link": url_for(".get_meta_key", meta_key=meta_key, page_number=1)
            }
        ]
        return render_template("meta_list.html", pagination=pagination, meta_to_be_displayed=meta_to_be_displayed, seo=seo, breadcrumbs=breadcrumbs)
    else:
        return "None found"


@app.route('/<string:meta_key>/<string:meta_val>/page/<int:page_number>/')
def get_meta_value(meta_key, meta_val, page_number):
    seo = {
        "title": "watch youtube videos of music charts available in " + meta_key + " : " + meta_val + " page " + str(page_number),
        "keywords": "music, charts, billboard, youtube, video, hot 100, page " + str(page_number) + ", " + meta_key + ", " + meta_val,
        "description": "watch the top music videos trending on music charts automatically."
                       "track the top music charts available in your " + meta_key + " : " + meta_val + " page " + str(page_number)
    }
    stations = db.stations.find({"meta." + meta_key: meta_val})
    count = stations.count()
    if count > (page_number - 1) * PER_PAGE:
        #should return list of objects divided by page
        stations_to_be_displayed = stations[(page_number - 1) * PER_PAGE:page_number * PER_PAGE]
        station_urls = create_url_objects_from_stations(stations_to_be_displayed)
        pagination = Pagination(page_number, PER_PAGE, count)
        meta_key_pos = db.stations.distinct("meta." + meta_key).index(meta_val)
        meta_page_number = meta_key_pos/PER_PAGE + 1
        breadcrumbs = [
            {
                "name": "home",
                "link": url_for(".index")
            },
            {
                "name": meta_key,
                "link": url_for(".get_meta_key", meta_key=meta_key, page_number=meta_page_number)
            },
            {
                "name": meta_val,
                "link": url_for(".get_meta_value", meta_key=meta_key, meta_val=meta_val, page_number=1)
            }
        ]
        return render_template("station_list.html", pagination=pagination, stations=station_urls, seo=seo, breadcrumbs=breadcrumbs)
    else:
        return "None found"


@app.route('/station/<string:name>/')
def station_details(name):
    station = db.stations.find_one({"name": name})
    if station:
        keywords = video_text_from_url(station["url"], station["settings"], station["soup_path_for_list"],
                                       station["soup_path_for_keyword"])
        videos = []
        seo = {
            "title": "watch youtube videos of " + station["display_name"],
            "keywords": ",".join(keywords),
            "description": "watch the top music videos trending on music charts automatically."
                           "track the top youtube videos of " + station["display_name"]
        }
        meta_key_pos = db.stations.distinct("name").index(name)
        meta_page_number = meta_key_pos/PER_PAGE + 1
        breadcrumbs = [
            {
                "name": "home",
                "link": url_for(".index")
            },
            {
                "name": "stations",
                "link": url_for(".stations", page_number=meta_page_number)
            },
            {
                "name": station["display_name"],
                "link": url_for(".station_details", name=name)
            }
        ]
        for keyword in keywords:
            videos.append(get_video_from_keyword(keyword))
        return render_template("station.html", videos=videos, seo=seo, breadcrumbs=breadcrumbs)
    #get the radio station from the object
    #get keywords from the object parameter
    else:
        return "Incomplete function"

@app.route('/stations/page/<int:page_number>/')
def stations(page_number):
    station_list = db.stations.find()
    count = station_list.count()
    if station_list:
        seo = {
            "title": "watch youtube videos of top charts page " + str(page_number),
            "keywords": "youtube playlist, music charts, automatic playlist",
            "description": "watch the top music videos trending on music charts automatically."
                           "track the top youtube videos of your favorite music page " + str(page_number)
        }
        stations_to_be_displayed = station_list[(page_number - 1) * PER_PAGE:page_number * PER_PAGE]
        pagination = Pagination(page_number, PER_PAGE, count)
        station_urls = create_url_objects_from_stations(stations_to_be_displayed)
        breadcrumbs = [
            {
                "name": "home",
                "link": url_for(".index")
            },
            {
                "name": "stations",
                "link": url_for(".stations", page_number=1)
            }
        ]
        return render_template("station_list.html", pagination=pagination, stations=station_urls, seo=seo, breadcrumbs=breadcrumbs)
    #get the radio station from the object
    #get keywords from the object parameter
    else:
        return "Incomplete function"

@app.route('/test/js/')
def station_detail_test():
    seo = {
        "title": "testing of player js",
        "keywords": "",
        "description": "testing result of player js"
    }
    return render_template("js_test.html", seo=seo)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page
app.jinja_env.globals['url_for'] = url_for
