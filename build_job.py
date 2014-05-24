from settings import *
from functions import *

browser = webdriver.Firefox()
browser = sign_in(browser, url, password_field, PASS, email_field, EMAIL, button, wait_box)
branch_num = find_project(PROJECT_URL, browser, name, class_name, id_name)
url = browser.find_elements_by_class_name(url_class)[branch_num].get_attribute('href')
browser.get(url)
browser.find_element_by_class_name('run_again').click()


browser.quit()