from bs4 import BeautifulSoup
import requests
import re


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
