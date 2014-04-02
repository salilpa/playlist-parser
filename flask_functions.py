from settings import PER_PAGE
from flask import url_for, request


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