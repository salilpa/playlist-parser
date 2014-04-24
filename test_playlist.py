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

    rv = test_app.get('/station/radioMirchiTvmMalayalamTop20', follow_redirects=True)
    expected_station_data = "globalcharts.tv"
    assert expected_station_data in rv.data

    rv = test_app.get('/station/wrongName', follow_redirects=True)
    expected_station_data = "Incomplete function"
    assert rv.data == expected_station_data

    rv = test_app.get('/', follow_redirects=True)
    expected_station_data = "globalcharts.tv"
    assert expected_station_data in rv.data

    rv = test_app.get('/stations/page/1', follow_redirects=True)
    expected_station_data = "globalcharts.tv"
    assert expected_station_data in rv.data


def test_generate_meta_key_urls():
    with playlist.app.test_request_context():
        attr_result = flask_functions.generate_meta_key_urls(db, "country")
    assert len(attr_result) > 0
    for indv_url in attr_result:
        rv = test_app.get(indv_url["url"])
        assert rv.status_code == 200

def test_create_url_objects_from_stations():
    station = db.stations.find()[:4]
    length_of_station = 4
    with playlist.app.test_request_context():
        result = flask_functions.create_url_objects_from_stations(station)
    assert len(result) == length_of_station