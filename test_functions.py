from functions import *
from settings import *


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
    assert "videoId" in get_video_from_keyword("poovin maarile")


def test_get_suggested_keyword():
    assert "" == get_suggested_keyword("fjghkkdhfgjdk")
    assert "" != get_suggested_keyword("poovin maarile")


def test_get_tag():
    browser = webdriver.Firefox()
    browser.get("https://www.codeship.io/")
    assert type(get_tag('Sign in', browser, "sign_in_email")) is WebElement
    assert get_tag('Sign in blah', browser, "sign_in_email") is False
    assert get_tag('Sign in', browser, "blah_email") is False
    browser.quit()


def test_sign_in():
    browser = webdriver.Firefox()
    assert sign_in(browser, url, password_field, "blah", "blah", "blah@blah.com", button, wait_box) is False
    assert sign_in(browser, url, "blah", "blah", email_field, "blah@blah.com", button, wait_box) is False
    assert sign_in(browser, url, password_field, PASS, email_field, EMAIL, "blah", wait_box) is False
    assert type(sign_in(browser, url, password_field, PASS, email_field, EMAIL, button, wait_box)) is webdriver.Firefox
    browser.quit()


def test_has_next_page():
    browser = webdriver.Firefox()
    sign_in(browser, url, password_field, PASS, email_field, EMAIL, button, wait_box)
    browser.get(PROJECT_URL)
    assert has_next_page(browser, "blah") is False
    assert type(has_next_page(browser, "older")) is unicode
    browser.quit()


def test_find_project():
    browser = webdriver.Firefox()
    sign_in(browser, url, password_field, PASS, email_field, EMAIL, button, wait_box)
    assert find_project(PROJECT_URL, browser, name, "blah_name", "blah_name") is False
    assert find_project(PROJECT_URL, browser, name, class_name, "blah_name") is False
    assert type(find_project(PROJECT_URL, browser, name, class_name, id_name)) is WebElement
    assert type(find_project(PROJECT_URL, browser, "jsTesting", class_name, id_name)) is WebElement
    browser.quit()
