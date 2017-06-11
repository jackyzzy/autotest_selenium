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



#edit cdn operation
select_items=browser.find_elements_by_class_name("checkbox-wrap")
if select_items[4].get_attribute("checked") is None:
    select_items[4].click()
    time.sleep(1)
    more_button=browser.find_element_by_css_selector(".btn.btn-small.dropdown-toggle")
    delete_button=browser.find_element_by_css_selector(".btn.dropdown-item.btn-host-force-shut-down")
    edit_button=browser.find_element_by_css_selector(".btn.dropdown-item.btn-host-reset")
    more_button.click()
    time.sleep(1)
    edit_button.click()
    time.sleep(1)
    remark_area=browser.find_element_by_name("remark")
    remark_content=random.sample('abcdefrshkoipqel',10)
    remark_area.send_keys(remark_content)
    time.sleep(1)
originsite=browser.find_elements_by_xpath("//span[@class='caret']")[1]
originsite.click()
def origin_doamin():
    select_domain=browser.find_element_by_xpath("//li[@data-value='domainName']")
    select_domain.click()
    domainname = browser.find_element_by_name('domainName')
    domainname_value = "www." + ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 8)) + ".com"
    domainname.send_keys(domainname_value)

def origin_ip():
    select_ip=browser.find_element_by_xpath("//li[@data-value='ipAddress']")
    select_ip.click()
    ipcontent=browser.find_element_by_name('ipAddress')
    ipcontent_value=str(random.randint(1,100))+'.'+str(random.randint(1,200))+\
                    '.'+str(random.randint(1,200))+'.'+str(random.randint(1,200))
    ipcontent.send_keys(ipcontent_value)

origin_parameter=random.randint(1,2)

if origin_parameter==1:
    origin_doamin()
elif origin_parameter==2:
    origin_ip()

time.sleep(1)
resource_host=browser.find_elements_by_xpath("//span[@class='caret']")[2]
resource_host.click()

def custom_host():
    host_input = browser.find_element_by_xpath("//li[@data-value='custom']")
    host_input.click()
    input_position = browser.find_element_by_name('setHost')
    input_content = random.sample('abcdefghijklmnopqrstuvwxyz',8)
    input_position.send_keys(input_content)

custom_parameter = random.randint(1,3)
if custom_parameter==1:
     custom_host()

time.sleep(2)
submit=browser.find_element_by_css_selector('.btn.btn-submit.btn-primary')
submit.click()

time.sleep(2)
browser.quit()