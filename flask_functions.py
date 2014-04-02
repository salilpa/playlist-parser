from settings import PER_PAGE
from flask import url_for

def generate_meta_key_urls(db, attr, value=None, size=4):
    if value:
        attr_keys = db.stations.find({"meta." + attr: value})[:size]
        attr_keys_length = attr_keys.count()
    else:
        attr_keys = db.stations.distinct("meta." + attr)[:size]
        attr_keys_length = len(attr_keys)

    urls = []
    for i in range(0, attr_keys_length/PER_PAGE + 1):
        if value:
            urls.append(url_for(".get_meta_value", meta_key = attr, meta_val=value, page_number=i+1))
        else:
            urls.append(url_for(".get_meta_key", meta_key = attr, page_number=i+1))
    return urls