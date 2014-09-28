from bs4 import BeautifulSoup
import requests
import re
from apiclient.discovery import build
from settings import DEVELOPER_KEY
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import selenium.webdriver.support.ui as ui

#returns a list of keywords from the url given using the soup paths
def video_text_from_url(url, settings, soup_path_for_list, soup_path_for_keyword):
    r = requests.get(url=url, headers=settings["headers"])
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, settings["parser"])
        keyword_list = []
        for article in soup.find_all(soup_path_for_list["tag"], soup_path_for_list["attr"]):
            keyword = []
            for soup_keywords in soup_path_for_keyword["paths"]:
                attribute = article.find(soup_keywords["tag"], soup_keywords["attr"])
                if attribute:
                    keyword.append(re.sub('[^A-Za-z0-9 ]+', '', attribute.text))
            keyword_list.append(" ".join(keyword))
        return keyword_list
    else:
        return []


def get_video_from_keyword(keyword):
    video = {
        "keyword": keyword
    }
    youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(q=keyword, part="id,snippet", maxResults="1", type="video", videoEmbeddable="true").execute()
    for search_result in search_response.get("items", []):
        video["videoId"] = search_result["id"]["videoId"]
        video["thumbnail"] = search_result["snippet"]["thumbnails"]["medium"]["url"]
        video["title"] = search_result["snippet"]["title"]
        video["description"] = search_result["snippet"]["description"]
    if not search_response.get("items", []):
        suggested_keyword = get_suggested_keyword(keyword)
        if keyword != "":
            video = get_video_from_keyword(suggested_keyword)
    return video


def get_suggested_keyword(keyword):
    url = "https://www.youtube.com/results"
    payload = {
        "search_query": keyword
    }
    result = requests.get(url, params=payload)
    if result.status_code == 200:
        soup = BeautifulSoup(result.text)
        title = soup.find("a", {"class": "yt-uix-tile-link"})
        if title:
            return title.text.strip()
        else:
            return ""
    else:
        return ""


def get_tag(name, browser, class_name):
    i = 0
    for tag in browser.find_elements_by_class_name(class_name):
        if tag.text == name:
            return i
        i += 1
    return False


def has_next_page(browser, id_name):
    try:
        id = browser.find_element_by_id(id_name)
        return id.get_attribute('href')
    except NoSuchElementException as e:
        return False


def sign_in(browser, url, password_field, password, email_field, email, button, wait_box):
    wait = ui.WebDriverWait(browser, 10)
    browser.get(url)

    try :
        email_box = browser.find_element_by_id(email_field)
        email_box.send_keys(email)
        password_box = browser.find_element_by_id(password_field)
        password_box.send_keys(password)
        buttons = browser.find_elements_by_name(button)
        if buttons:
            browser_button = buttons[0]
            browser_button.click()
        else:
            return False
    except NoSuchElementException as e:
        return False

    wait.until(lambda browser: browser.find_elements_by_class_name(wait_box))

    return browser


def find_project(project_url, browser, name, class_name, id_name):
    browser.get(project_url)
    while True:
        tag = get_tag(name, browser, class_name)
        if tag is not False:
            return tag
        else:
            next_page = has_next_page(browser, id_name)
            if next_page:
                browser.get(next_page)
            else:
                break
    return False