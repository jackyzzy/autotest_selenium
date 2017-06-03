
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
addbutton = browser.find_element_by_css_selector('.btn.btn-differ.btn-small')
addbutton.click()
time.sleep(1)

length = random.randint(3, 5)
sethost_value = random.sample('abcdefghijklmnopqrstuvwxyz.', length)

# input the accelerate domain
domain = browser.find_element_by_name('domain')
domain_value = "www." + \
    ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', length)) + ".com"
domain.send_keys(domain_value)
time.sleep(1)

# input the description message
remark = browser.find_element_by_name('remark')
remark_value = random.sample('abcdefghijklmnopqrstuvwxyz', 10)
remark.send_keys(remark_value)
time.sleep(1)

# select the kind of acceleration randomly
acceleoptions = browser.find_elements_by_xpath("//span[@class='caret']")[0]
acceleoptions.click()


def large_file():
    video_audio = browser.find_element_by_xpath("//li[@data-value='10']")
    video_audio.click()


def muti_media():
    video_audio = browser.find_element_by_xpath("//li[@data-value='11']")
    video_audio.click()


def tiny_file():
    video_audio = browser.find_element_by_xpath("//li[@data-value='12']")
    video_audio.click()

acce_parameter = random.randint(1, 3)
if acce_parameter == 1:
    large_file()
elif acce_parameter == 2:
    muti_media()
elif acce_parameter == 3:
    tiny_file()

time.sleep(1)

# select the origin site options randomly
originsite = browser.find_elements_by_xpath("//span[@class='caret']")[1]
originsite.click()


def origin_doamin():
    select_domain = browser.find_element_by_xpath(
        "//li[@data-value='domainName']")
    select_domain.click()
    domainname = browser.find_element_by_name('domainName')
    domainname_value = "www." + \
        ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', length)) + ".com"
    domainname.send_keys(domainname_value)


def origin_ip():
    select_ip = browser.find_element_by_xpath("//li[@data-value='ipAddress']")
    select_ip.click()
    ipcontent = browser.find_element_by_name('ipAddress')
    ipcontent_value = str(random.randint(1,
                                         100)) + '.' + str(random.randint(1,
                                                                          200)) + '.' + str(random.randint(1,
                                                                                                           200)) + '.' + str(random.randint(1,
                                                                                                                                            200))
    ipcontent.send_keys(ipcontent_value)

origin_parameter = random.randint(1, 2)

if origin_parameter == 1:
    origin_doamin()
elif origin_parameter == 2:
    origin_ip()

time.sleep(1)

# select the origin host randomly
resource_host = browser.find_elements_by_xpath("//span[@class='caret']")[2]
resource_host.click()


def custom_host():
    host_input = browser.find_element_by_xpath("//li[@data-value='custom']")
    host_input.click()
    input_position = browser.find_element_by_name('setHost')
    input_content = random.sample('abcdefghijklmnopqrstuvwxyz', 8)
    input_position.send_keys(input_content)

custom_parameter = random.randint(1, 3)
if custom_parameter == 1:
    custom_host()


# submit the add operation
time.sleep(2)
submit = browser.find_element_by_css_selector('.btn.btn-submit.btn-primary')
submit.click()

time.sleep(2)
browser.quit()
