from flask import Flask, request
from functions import *
import json
from decorator import crossdomain

app = Flask(__name__)


#returns a page with links to all websites
@app.route('/', methods=["POST", "GET", "OPTIONS"])
@crossdomain(origin='*')
def index():
    if request.method == 'POST':
        station = json.loads(request.form["data"])
        return ",".join(video_text_from_url(station["url"], station["settings"], station["soup_path_for_list"], station["soup_path_for_keyword"]))
    else:
        return "All is well"