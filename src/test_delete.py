from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
#import selenium.JavascriptExecutor
import time
import random
from selenium.webdriver.common.action_chains import *
from selenium.webdriver.support.select import Select

browser = webdriver.Chrome()  # Get local session of firefox
browser.get("http://100.1.22.3/dashboard/cdn/#cdn")  # Load page

# login input username and password
username = browser.find_element_by_id('id_username')
username.send_keys('acloud@sangfor.com')
password = browser.find_element_by_id('id_password')
password.send_keys('Admin12345')
loginbutton = browser.find_element_by_id('loginBtn')
loginbutton.click()
time.sleep(2)

# select cdn and switch to the cdn dashboard page
presenthandle = browser.current_window_handle
browser.switch_to.window(presenthandle)
cdnnavi = browser.find_element_by_id('hd-nav-product')
chain = ActionChains(browser)
chain.move_to_element(cdnnavi).perform()
browser.get("http://100.1.22.3/dashboard/cdn/#cdn")
time.sleep(2)


# enter the cdn dashboard page and implement operations
secondhandle = browser.current_window_handle
browser.switch_to.window(secondhandle)
time.sleep(1)


# delete cdn operation
select_items = browser.find_elements_by_class_name("checkbox-wrap")
select_num = random.randint(1, 3)
select_items[select_num].click()
time.sleep(1)
more_button = browser.find_element_by_css_selector(
    ".btn.btn-small.dropdown-toggle")
more_button.click()
time.sleep(1)
delete_button = browser.find_element_by_css_selector(
    ".btn.dropdown-item.btn-host-force-shut-down")
delete_button.click()
time.sleep(2)
confirm_delete = browser.find_element_by_css_selector(
    '.btn.btn-submit.btn-primary')
confirm_delete.click()

time.sleep(2)
browser.quit()
