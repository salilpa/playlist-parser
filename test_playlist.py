import playlist
import requests
import json
import flask_functions
from mock import MagicMock
from settings import db


def get_stub(*args, **kwargs):
    response = requests.get.return_value
    with open('radio983.html', 'r') as f:
        response.text = f.read()
        response.status_code = 200
        return response

requests.get = MagicMock(side_effect=get_stub)

test_app = playlist.app.test_client()


def test_website():
    payload = {
        "name": "radioMirchiTvmMalayalamTop20",
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
        },
        "meta": {
            "country": "india",
            "language": "malayalam",
        }
    }
    rv = test_app.post('/pageToKeywords/', data=json.dumps(payload))
    expected_data = ['MARIVIL  DRISHYAM', 'KAATTU MOOLIYO OM SHANTHI OSANA ', 'OLANJAALI KURUVIL 1983', 'EERAN KAATTIN  SALALA MOBILES', 'MANDARAME OM SHANTHI OSANA ', 'KANNADI VATHIL LONDON BRIDGE', 'OMANA POOVE ORU INDIAN PRANAY', 'RASOOL ALLAH SALALA MOBILES', 'PUNCHIRI THANCHUM BYCYCLE THIEVES', 'LA LA LASA SALALA MOBILES', 'AASHICHAVAN PUNYALAN AGARBATTIS', 'NENJILE NENJILE 1983', 'THAMARAPOONKAVANAT BALYAKALA SAKHI', 'CHEMMANA CHELORUKKI MANNAR MATHAI SPE', 'THALAVATTOM 1983', 'THIRIYAANE MANNAR MATHAI SPE', 'MADHUMATHI GEETHANJALI', 'CHINNI CHINNI LONDON BRIDGE', 'THEERATHE NEELUNNE THIRA', 'OTTEKKU PAADUNNA NADAN']
    assert rv.data.split("|") == expected_data
    
    rv = test_app.get('/pageToKeywords/')
    expected_get_data = "All is well"
    assert rv.data == expected_get_data

    rv = test_app.get('/station/radioMirchiTvmMalayalamTop20')
    expected_station_data = "total number of videos is 20"
    assert rv.data == expected_station_data

    rv = test_app.get('/station/wrongName')
    expected_station_data = "Incomplete function"
    assert rv.data == expected_station_data

    rv = test_app.get('/')
    expected_station_data = "dummy index function"
    assert rv.data == expected_station_data


def test_generate_meta_key_urls():
    with playlist.app.test_request_context():
        result = flask_functions.generate_meta_key_urls(db, "country")
    for indv_url in result:
        rv=test_app.get(indv_url)
        assert rv.status_code == 200