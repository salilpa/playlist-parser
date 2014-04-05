from functions import *


def test_video_text_from_url():
    payload = {
        "url": 'http://www.radiomirchi.com/thiruvananthapuram/countdown/malayalam-top-20',
        "settings": {
            "parser": "html5lib",
            "headers": {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0",
            }
        },
        "soup_path_for_list": {
            "tag": "div",
            "attr": {
                "class": "mirchi_20_box2"
            }
        },
        "soup_path_for_keyword": {
            "paths": [
                {
                    "tag": "span",
                    "attr": {
                        "class": "or12"
                    }
                },
                {
                    "tag": "span",
                    "attr": {
                        "class": "moviename"
                    }
                },
            ]
        }
    }
    keywords = video_text_from_url(payload["url"], payload["settings"], payload["soup_path_for_list"],
                                   payload["soup_path_for_keyword"])
    assert len(keywords) == 20
    payload["soup_path_for_list"]["attr"]["class"] = "blah"
    keywords = video_text_from_url(payload["url"], payload["settings"], payload["soup_path_for_list"],
                                   payload["soup_path_for_keyword"])
    assert len(keywords) == 0


def test_get_video_from_keyword():
    assert "videoId" in get_video_from_keyword("dil se")
    assert "videoId" not in get_video_from_keyword("hvjhdvhbdhfbvjhdfbvd")
    assert "videoId" in get_video_from_keyword("poovin maarile")


def test_get_suggested_keyword():
    assert "" == get_suggested_keyword("fjghkkdhfgjdk")
    assert "" != get_suggested_keyword("poovin maarile")