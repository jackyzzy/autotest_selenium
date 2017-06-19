# coding=utf-8
from selenium import webdriver
from time import sleep
from random import randint
import instance
import config

class Volume():
    ''' volume test case
    >>> pp = "http://100.86.0.1"
    
    >>> vol = 'vvv'
    
    >>> disk = Volume(pp)
    
    >>> sleep(5)
    
    >>> disk.login()
        
    >>> disk.umount(vol)
    True
    >>> sleep(5)
    
    >>> disk.expandVoluem(vol, 10)
    True
    
    >>> disk.mountVolumeToInstance(vol, 'test96')
    True
    >>> disk.logout()
    
    '''
    def __init__(self, plate):
        self.plate = plate
        self.host = config.host
        self.disk = config.disk
        self.userName = config.userName
        self.passwd = config.passwd
        self.volBase = config.volBase
        self.volcnt = randint(2,100)
        self.driver = webdriver.Chrome()
        self.volList = self.getVolumeList()
        
    def login(self):
        ''' login '''
        driver = self.driver
        driver.get(self.plate)
        driver.delete_all_cookies()
        driver.refresh()
        
        driver.find_element_by_id("id_username").send_keys(self.userName)
        driver.find_element_by_id("id_password").send_keys(self.passwd)
        driver.find_element_by_id("loginBtn").click()
        sleep(0.5)

    def getVolumeList(self):
        ''' get volume list '''
        
        driver = webdriver.Chrome()
        volList = []
        
        driver.get(self.plate + self.disk)
        driver.delete_all_cookies()
        driver.refresh()

        ''' login '''
        driver.find_element_by_id("id_username").send_keys(self.userName)
        driver.find_element_by_id("id_password").send_keys(self.passwd)
        driver.find_element_by_id("loginBtn").click()
        
        # go to disk page
        driver.get(self.plate + self.disk)
        sleep(2)
        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return volList
            volName = td.find_element_by_xpath('.//td[3]/div').text
            volList.append(volName)
            
        driver.quit()
        return volList

    def logout(self):
        driver = self.driver
        ''' clear env '''
        driver.quit()
        
    def createVolume(self, volName, speed = None, size = None):
        assert volName != None
        assert speed != None
        assert size >= 50
        
        driver = self.driver
        driver.get(self.plate + self.disk)
        sleep(2)
        
        '''click add volume'''
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/button[1]').click()
        sleep(0.5)
        
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[1]/div/input').send_keys(volName)
        sleep(0.3)
        if speed == None or speed == 'ultra':
#             ultrx speed
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[3]/div/ul/li[1]').click()
        else:
#             high speed
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[3]/div/ul/li[2]').click()
        sleep(0.5)
            
        if size == None:
            assert size >= 50
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[4]/div[1]/div/input').send_keys(size)
            sleep(0.5)

#         click create
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        self.volList.append(volName)
        sleep(1)
        return True
    
    def expandVoluem(self, volName, size):
        ''' 
        expand volume 
        '''
        assert len(self.volList) != 0
        assert size > 0
        assert volName != None and volName in self.volList
        
        driver = self.driver
        # go to plate page
        driver.get(self.plate + self.disk)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return False
            
            target = td.find_element_by_xpath('.//td[3]/div')
            if target.text != volName:
                continue
            
            status = td.find_element_by_xpath(".//td[2]/div").get_attribute('title')
            if status != '未挂载':
                print ('volume status is still in use. status is %s' %(status))
                return False
            
            checkLable = td.find_element_by_xpath(".//td[1]/label")
            checkLable.click()
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/button[2]').click()
            sleep(0.5)
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[3]/div/input').clear()
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[3]/div/input').send_keys(size)
            sleep(1)
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
            sleep(1)
            return True
        return False    
    def deleteVolume(self, volName, delBackup = False):
        ''' 
        delete volume 
        '''
        assert len(self.volList) != 0
        assert volName != None and volName in self.volList
        
        driver = self.driver
        # go to plate page
        driver.get(self.plate + self.disk)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return False
            
            target = td.find_element_by_xpath('.//td[3]/div')
            if target.text != volName:
                continue
            
            checkLable = td.find_element_by_xpath(".//td[1]/label")
            checkLable.click()
            driver.find_element_by_xpath('//*[@id="storage-disk-more-action"]').click()
            sleep(0.5)
            driver.find_element_by_xpath('//*[@id="content-body"]/div/div[1]/div[1]/ul/li[5]/button').click()
            sleep(1)
            if delBackup : 
                driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/label/label').click()
                sleep(5)
            driver.find_element_by_xpath('//*[@id="common-widget-messagebox-checkbox-ok"]').click()
            sleep(1)
            self.volList.remove(volName)
            return True
        
        return False
    
    def mountVolumeToInstance(self, volName, vmName):
        ''' mount volume to instance '''
        
        assert len(self.volList) != 0
        assert volName != None and vmName != None
        
        '''
        check if the instance is still running
        '''
        inc = instance.Instance(self.plate)
        inc.login()
        if inc.getInstanceStatus(vmName) != '已关机':
            print('can not umount for instanc, instance[%s] is still runnint' %(vmName))
            inc.logout()
            return False
        inc.logout()
        
        
        driver = self.driver
        driver.get(self.plate + self.disk)
        sleep(2)
        
        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            if td.text == "没有找到匹配的记录":
                return False
            target = td.find_element_by_xpath('.//td[3]/div')
            if target.text != volName:
                continue
            status = td.find_element_by_xpath(".//td[2]/div").get_attribute('title')
            if status != '未挂载':
                print ('volume status no in use. status is %s' %(status))
                return False
                        
            checkLable = td.find_element_by_xpath(".//td[1]/label")
            checkLable.click()
            break
        
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/button[3]').click()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[2]/div/div/span').click()
        sleep(1)
        ul = driver.find_elements_by_xpath('/html/body/div[6]/div/ul/li')
        for li in ul:
            if li.text == vmName:
                li.click()
                sleep(0.5)
                driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
                sleep(3)
                return True
            
        return False
    
    def umount(self, volName):
        ''' 
        unmount volume from instance
        '''
        
        assert len(self.volList) != 0
        assert volName != None and volName in self.volList
        
        driver = self.driver
        # go to plate page
        driver.get(self.plate + self.disk)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return False
            
            target = td.find_element_by_xpath('.//td[3]/div')
            if target.text != volName:
                continue
            
            status = td.find_element_by_xpath(".//td[2]/div").get_attribute('title')
            if status != '正在使用':
                print ('volume status no in use. status is %s' %(status))
                return False
            
            checkLable = td.find_element_by_xpath(".//td[1]/label")
            checkLable.click()
            
            '''
            check if the instance is still running
            '''
            inc = instance.Instance(self.plate)
            vm = td.find_element_by_xpath(".//td[8]/div").text
            inc.vmlist.append(vm)
            inc.login()
            if inc.getInstanceStatus(vm) != '已关机':
                print('can not umount for instanc, instance[%s] is still runnint' %(vm))
                inc.logout()
                return False
            inc.logout()
            
            driver.find_element_by_xpath('//*[@id="storage-disk-more-action"]').click()
            sleep(0.5)
            driver.find_element_by_xpath('//*[@id="content-body"]/div/div[1]/div[1]/ul/li[1]/button').click()
            sleep(1)
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
            sleep(5)
            return True
        
        return False

if __name__ == "__main__":
    import doctest
    doctest.testmod()