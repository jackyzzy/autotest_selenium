from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
#import selenium.JavascriptExecutor
import time
import random
from selenium.webdriver.common.action_chains import *
from selenium.webdriver.support.select import Select

browser = webdriver.Chrome() # Get local session of firefox
browser.get("http://100.1.22.3/dashboard/cdn/#cdn") # Load page

#login input username and password
username=browser.find_element_by_id('id_username')
username.send_keys('acloud@sangfor.com')
password=browser.find_element_by_id('id_password')
password.send_keys('Admin12345')
loginbutton=browser.find_element_by_id('loginBtn')
loginbutton.click()
time.sleep(2)

#select cdn and switch to the cdn dashboard page
presenthandle=browser.current_window_handle
browser.switch_to.window(presenthandle)
cdnnavi=browser.find_element_by_id('hd-nav-product')
chain=ActionChains(browser)
chain.move_to_element(cdnnavi).perform()
browser.get("http://100.1.22.3/dashboard/cdn/#cdn")
time.sleep(2)


#enter the cdn dashboard page and implement operations
secondhandle=browser.current_window_handle
browser.switch_to.window(secondhandle)
time.sleep(1)

#stop cdn operation
select_item_se = browser.find_element_by_css_selector(
        "tr[data-index='3'] td[class='bs-checkbox'] label[class='checkbox-wrap']")
select_item_se.click()
time.sleep(1)
stopbutton = browser.find_element_by_xpath("//button[@action='stop']")
startbutton = browser.find_element_by_xpath("//button[@action='start']")
situation = browser.find_element_by_css_selector("tr[data-index='3'] span")

if situation.get_attribute("class") == "host-list-icon iconfont icon-state-ctrlplay":
    stopbutton.click()
    time.sleep(1)
    confirm_stop = browser.find_element_by_css_selector(".btn.btn-submit.btn-primary")
    confirm_stop.click()
elif situation.get_attribute("class") == "host-list-icon iconfont icon-ctrlpause cdn-icon-pause":
    startbutton.click()

time.sleep(2)
browser.quit()



