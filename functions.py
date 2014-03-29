from bs4 import BeautifulSoup
import requests
import re
from apiclient.discovery import build
from settings import DEVELOPER_KEY


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
    video = {}
    youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(q=keyword, part="id,snippet", maxResults="1", type="video").execute()
    for search_result in search_response.get("items", []):
        video["videoId"] = search_result["id"]["videoId"]
        video["thumbnail"] = search_result["snippet"]["thumbnails"]["medium"]["url"]
        video["title"] = search_result["snippet"]["title"]
        video["description"] = search_result["snippet"]["description"]
    return video