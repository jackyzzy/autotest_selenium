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

# input the accelerate domain
domain = browser.find_element_by_name('domain')
current_time = time.strftime('%d%H%M%S', time.localtime(time.time()))
domain_value = "www.youku" + current_time + ".com"
domain.send_keys(domain_value)
time.sleep(1)

# input the description message
remark = browser.find_element_by_name('remark')
remark_value = "movie sites"
remark.send_keys(remark_value)
time.sleep(1)

# select the kind of accelerate(file download file)
acceleoptions = browser.find_elements_by_xpath("//span[@class='caret']")[0]
acceleoptions.click()
video_audio = browser.find_element_by_xpath("//li[@data-value='10']")
video_audio.click()
time.sleep(1)

# select the origin site options randomly(domainname)
originsite = browser.find_elements_by_xpath("//span[@class='caret']")[1]
originsite.click()

select_domain = browser.find_element_by_xpath("//li[@data-value='domainName']")
select_domain.click()

domainname = browser.find_element_by_name('domainName')
domainname_value = "www.dytt8.net"
domainname.send_keys(domainname_value)
time.sleep(1)

# select the origin host randomly(custom)
resource_host = browser.find_elements_by_xpath("//span[@class='caret']")[2]
resource_host.click()
huiyuan_host = browser.find_element_by_css_selector("li[data-value='custom']")
huiyuan_host.click()
custom_host = browser.find_element_by_css_selector("input[name='setHost']")
custom_hostname = "www.ygdy8.net"
custom_host.send_keys(custom_hostname)

# submit the add operation
time.sleep(1)
submit = browser.find_element_by_css_selector('.btn.btn-submit.btn-primary')
submit.click()
time.sleep(1)


# stop the cdn and edit information
select_item = browser.find_element_by_css_selector(
    "tr[data-index='0'] td[class='bs-checkbox'] label[class='checkbox-wrap']")
select_item.click()
time.sleep(1)
stopbutton = browser.find_element_by_xpath("//button[@action='stop']")
startbutton = browser.find_element_by_xpath("//button[@action='start']")
situation = browser.find_element_by_css_selector("tr[data-index='0'] span")
stopbutton.click()
time.sleep(1)
confirm_stop = browser.find_element_by_css_selector(
    ".btn.btn-submit.btn-primary")
confirm_stop.click()
time.sleep(1)

more_button = browser.find_element_by_css_selector(
    ".btn.btn-small.dropdown-toggle")
delete_button = browser.find_element_by_css_selector(
    ".btn.dropdown-item.btn-host-force-shut-down")
edit_button = browser.find_element_by_css_selector(
    ".btn.dropdown-item.btn-host-reset")
time.sleep(1)
more_button.click()
time.sleep(1)
edit_button.click()
time.sleep(1)
remark_area = browser.find_element_by_name("remark")
remark_content = "movies of all times"
remark_area.clear()
time.sleep(1)
remark_area.send_keys(remark_content)
time.sleep(1)
time.sleep(1)
domainname = browser.find_element_by_name('domainName')
domainname_value = "www.xiazaba.com"
domainname.clear()
time.sleep(1)
domainname.send_keys(domainname_value)
time.sleep(1)
custom_host_s = browser.find_element_by_name("setHost")
custom_content = "www.rar8.net"
custom_host_s.clear()
custom_host_s.send_keys(custom_content)

time.sleep(1)
submit = browser.find_element_by_css_selector('.btn.btn-submit.btn-primary')
submit.click()

# start the cdn accelerate and edit info again
time.sleep(2)
startbutton.click()
time.sleep(2)
more_button.click()
time.sleep(1)
edit_button.click()
time.sleep(1)
remark_s_area = browser.find_element_by_css_selector("textarea[name='remark']")
remark_content = "movies fans' favorite"
remark_s_area.clear()
time.sleep(1)
remark_s_area.send_keys(remark_content)
time.sleep(1)
domainname_value = "www.regus.cn"
domainname_area = browser.find_element_by_css_selector(
    "input[name='domainName']")
domainname_area.clear()
time.sleep(1)
domainname_area.send_keys(domainname_value)
time.sleep(1)
custom_host_t = browser.find_element_by_name("setHost")
custome_scontent = "www.lvseba.com"
custom_host_t.clear()
custom_host_t.send_keys(custome_scontent)

time.sleep(1)
submitbutton = browser.find_element_by_css_selector(
    '.btn.btn-submit.btn-primary')
submitbutton.click()

time.sleep(1)


# delete the cdn accelerate domain
more_button.click()
time.sleep(1)
delete_button = browser.find_element_by_css_selector(
    ".btn.dropdown-item.btn-host-force-shut-down")
delete_button.click()
time.sleep(1)
confirm_delete = browser.find_element_by_css_selector(
    '.btn.btn-submit.btn-primary')
confirm_delete.click()
time.sleep(2)
browser.quit()
