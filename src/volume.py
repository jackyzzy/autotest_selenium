# coding=utf-8
from selenium import webdriver
from time import sleep
from random import randint
import check

class Volume():
    ''' volume test case
    >>> pp = "http://100.86.0.1"
        
    >>> dd = "/dashboard/host/#host"
    
    >>> vol = 'vvv'
    
    >>> disk = Volume(pp, dd)
    
    >>> disk.login()
    
    >>> disk.createVolume(vol, 'high', 60)
    
    >>> sleep(10)
    
    >>> disk.logout()
    
    '''
    def __init__(self, plate, disk):
        self.plate = plate
        self.disk = disk
        self.volBase = "test"
        self.volList = []
        self.volcnt = randint(2,100)
        self.check = check.Check();
        self.driver = webdriver.Chrome()
    
    def login(self):
        driver = self.driver
        driver.get(self.plate)
        driver.delete_all_cookies()
        driver.refresh()
        
        ''' login '''
        driver.find_element_by_id("id_username").send_keys("zzy@sangfor.com")
#         driver.find_element_by_id("id_username").send_keys("acloud@sangfor.com")
        driver.find_element_by_id("id_password").send_keys("Admin12345")
        driver.find_element_by_id("loginBtn").click()
        sleep(0.5)
    
    def logout(self):
        driver = self.driver
        ''' clear env '''
        driver.quit()
    
    def createVolume(self, volname, speed = None, size = None):
        assert volname != None
        driver = self.driver
        driver.get(self.plate + self.disk)
        sleep(2)
        
        '''click add volume'''
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/button[1]').click()
        sleep(0.5)
        
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[1]/div/input').send_keys(volname)
        
        if speed == None or speed == 'ultra':
#             ultrx speed
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[3]/div/ul/li[1]').click()
        else:
#             high speed
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[3]/div/ul/li[2]').click()
            
        if size == None:
            assert size >= 50
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[4]/div[1]/div/input').send_keys(size)

#         click create
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
    
    def expandVoluem(self):
        pass
    
    def deleteVolume(self):
        pass
    
    def mount(self):
        pass
    
    def unmount(self):
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()