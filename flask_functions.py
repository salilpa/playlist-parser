from settings import PER_PAGE
from flask import url_for

def generate_meta_key_urls(db, attr):
    attr_keys = db.stations.distinct("meta" + attr)

    attr_keys_length = len(attr_keys)

    urls = []
    for i in range(0, attr_keys_length/PER_PAGE + 1):
        urls.append(url_for(".get_meta_key", meta_key = attr, page_number=i+1))

    return urls