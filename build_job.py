from settings import *
from functions import *

browser = webdriver.Firefox()
browser = sign_in(browser, url, password_field, PASS, email_field, EMAIL, button, wait_box)
find_project(PROJECT_URL, browser, name, class_name, id_name)
browser.get(PROJECT_URL)


browser.quit()