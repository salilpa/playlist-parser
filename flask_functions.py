from flask import request
from flask import url_for as flask_url_for


def url_for(endpoint, **kwargs):
    kwargs.setdefault('_external', True)
    return flask_url_for(endpoint, **kwargs)


def generate_meta_key_urls(db, attr, size=4):
    #returns urls for different value of a specific key
    #eg country returns urls for india and us

    attr_keys = db.stations.distinct("meta." + attr)[:size]

    urls = []
    for keys in attr_keys:
        urls.append({
            "name": keys,
            "url": url_for(".get_meta_value", meta_key=attr, meta_val=keys, page_number=1)
        })

    return urls


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page_number'] = page
    return url_for(request.endpoint, **args)


def create_url_objects_from_stations(stations):
    url_objects = []
    for station in stations:
        url_object ={}
        url_object["name"] = station["display_name"]
        url_object["url"] = url_for(".station_details", name=station["name"])
        url_object["parent_url"] = station["url"]
        url_object["meta"] = []
        for key, value in station["meta"].iteritems():
            url_for_key = url_for(".get_meta_key", meta_key = key, page_number =1)
            url_for_value = url_for(".get_meta_value", meta_key = key, meta_val = value, page_number=1)
            url_object["meta"].append({
                "key_url": url_for_key,
                "key_name": key,
                "val_url": url_for_value,
                "val_name": value
            })
        url_objects.append(url_object)
    return url_objects
