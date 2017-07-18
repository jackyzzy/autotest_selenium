# coding=utf-8
from selenium import webdriver
from time import sleep
from random import randint
import instance
import envConfig

class Volume():
    ''' volume test case
    >>> pp = "http://100.1.22.1"
    
    >>> disk = Volume(pp)
    
    >>> sleep(1)
    
    >>> disk.login()
        
    >>> disk.clearVolume()
    True
    >>> disk.logout()
    
    '''
    def __init__(self, plate):
        self.plate = plate
        self.host = envConfig.host
        self.disk = envConfig.disk
        self.userName = envConfig.userName
        self.passwd = envConfig.passWD
        self.volBase = envConfig.volBase
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

    def logout(self):
        driver = self.driver
        ''' clear env '''
        driver.quit()

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
        sleep(0.5)
        
        driver.get(self.plate + self.disk)
        sleep(2)
        trs = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录": 
            return volList
        for tr in trs:
            volName = tr.find_element_by_xpath('.//td[3]/div').text
            volList.append(volName) 
        driver.quit()
        return volList
    
    def getVolumeStatus(self, volName):
        ''' get volume status '''
        assert len(self.volList) != 0
        assert volName in self.volList
        
        driver = self.driver
        driver.get(self.plate + self.disk)
        sleep(2)

        trs = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录":
            print('volume list is empty')
            return None
        for tr in trs:
            target = tr.find_element_by_xpath('.//td[3]/div').text
            if target != volName:
                continue
            status = tr.find_element_by_xpath(".//td[2]/div").get_attribute('title')
            return status
        else:
            return None
    
    def createVolume(self, volName, speed = 'ultra', size = 50):
        ''' create volume '''
        assert volName != None
        assert size >= 50 and size <= 2048 
        
        driver = self.driver
        driver.get(self.plate + self.disk)
        sleep(2)
        
        '''click add volume'''
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/button[1]').click()
        sleep(0.5)
        
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[1]/div/input').send_keys(volName)
        sleep(0.3)
        if speed == 'ultra':
#             ultrx speed
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[3]/div/ul/li[1]').click()
        else:
#             high speed
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[3]/div/ul/li[2]').click()
        sleep(0.5)
            
        if size > 50:
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[4]/div[1]/div/input').send_keys(str(size))
            sleep(0.5)
            
#         click create
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        self.volList.append(volName)
        return True
    
    def expandVolume(self, volName, size):
        ''' expand volume '''
        assert len(self.volList) != 0
        assert size > 0
        assert volName != None and volName in self.volList
        
        driver = self.driver
        driver.get(self.plate + self.disk)
        sleep(2)

        trs = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录":
            print('volume list is empty')
            return False
        for tr in trs:
            target = tr.find_element_by_xpath('.//td[3]/div').text
            if target != volName:
                continue
            status = tr.find_element_by_xpath(".//td[2]/div").get_attribute('title')
            if status != '未挂载':
                print ('volume status is still in use. status is %s' %(status))
                return False
            tr.find_element_by_xpath(".//td[1]/label").click()
            sleep(0.5)
            break
        else:
            print('volume[%s] is not find in volume page' %(volName))
            return False            
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/button[2]').click()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[3]/div/input').clear()
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[3]/div/input').send_keys(str(size))
        sleep(1)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        return True
    
    def deleteVolume(self, volName, delBackup = True):
        ''' delete volume '''
        assert len(self.volList) != 0
        assert volName != None and volName in self.volList
        
        driver = self.driver
        driver.get(self.plate + self.disk)
        sleep(2)

        trs = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录": 
            print('volume list is empty')
            return False
        for tr in trs:
            target = tr.find_element_by_xpath('.//td[3]/div').text
            if target != volName:
                continue
            tr.find_element_by_xpath(".//td[1]/label").click()
            sleep(0.5)
            break
        else:
            print('volume[%s] is not find in volume page' %(volName))
            return False
        driver.find_element_by_xpath('//*[@id="storage-disk-more-action"]').click()
        sleep(0.5)
        driver.find_element_by_xpath('//*[@id="content-body"]/div/div[1]/div[1]/ul/li[5]/button').click()
        sleep(1)
        if delBackup : 
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/label/label').click()
            sleep(0.5)
        driver.find_element_by_xpath('//*[@id="common-widget-messagebox-checkbox-ok"]').click()
        sleep(1)
        self.volList.remove(volName)
        return True
    
    def mountVolumeToInstance(self, volName, vmName):
        ''' mount volume to instance '''        
        assert len(self.volList) != 0
        assert volName != None and vmName != None
        
        ''' check if the instance is still running '''
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
        
        trs = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录":
            print('volume list is empty')
            return False
        for tr in trs:
            target = tr.find_element_by_xpath('.//td[3]/div').text
            if target != volName:
                continue
            status = tr.find_element_by_xpath(".//td[2]/div").get_attribute('title')
            if status != '未挂载':
                print ('volume status no in use. status is %s' %(status))
                return False   
            tr.find_element_by_xpath(".//td[1]/label").click()
            sleep(0.5)
            break
        else:
            print('volume[%s] is not find in volume page' %(volName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/button[3]').click()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[2]/div/div/span').click()
        sleep(1)
        lis = driver.find_elements_by_xpath('/html/body/div[6]/div/ul/li')
        for li in lis:
            if li.text == vmName:
                li.click()
                sleep(0.5)
                break
        else:
            print('vm[%s] is not find in volume mount page' %(volName))                
            return False
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        return True
    
    def umount(self, volName):
        ''' unmount volume from instance '''
        assert len(self.volList) != 0
        assert volName != None and volName in self.volList
                
        driver = self.driver
        driver.get(self.plate + self.disk)
        sleep(2)

        trs = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录":
            print('volume list is empty')
            return False
        for tr in trs:
            target = tr.find_element_by_xpath('.//td[3]/div').text
            if target != volName:
                continue
            status = tr.find_element_by_xpath(".//td[2]/div").get_attribute('title')
            if status != '正在使用':
                print ('volume status no in use. status is %s' %(status))
                return False
            tr.find_element_by_xpath(".//td[1]/label").click()
            sleep(0.5)
            
            ''' check if the instance is still running '''
            inc = instance.Instance(self.plate)
            vm = tr.find_element_by_xpath(".//td[8]/div").text
            inc.vmlist.append(vm)
            inc.login()
            if inc.getInstanceStatus(vm) != '已关机':
                print('can not umount for instanc, instance[%s] is still runnint' %(vm))
                inc.logout()
                return False
            inc.logout()
            break
        else:
            print('volume[%s] is not find in volume page' %(volName))
            return False
        driver.find_element_by_xpath('//*[@id="storage-disk-more-action"]').click()
        sleep(0.5)
        driver.find_element_by_xpath('//*[@id="content-body"]/div/div[1]/div[1]/ul/li[1]/button').click()
        sleep(1)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(3)
        return True

    def createBackup(self, volName, backupName = 'manual'):
        ''' create backup '''
        assert len(self.volList) != 0
        assert volName != None and volName in self.volList
        
        driver = self.driver
        driver.get(self.plate + self.disk)
        sleep(2)

        trs = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录":
            print('volume list is empty')
            return False
        for tr in trs:
            target = tr.find_element_by_xpath('.//td[3]/div').text
            if target != volName:
                continue
            status = tr.find_element_by_xpath(".//td[2]/div").get_attribute('title')
            if status != '正在使用':
                print ('volume status no in use. status is %s' %(status))
                return False
            tr.find_element_by_xpath(".//td[1]/label").click()
            sleep(0.5)
            break
        else:
            print('volume[%s] is not find in volume page' %(volName))
            return False
        driver.find_element_by_xpath('//*[@id="storage-disk-more-action"]').click()
        sleep(0.5)
        backupBtn = driver.find_element_by_xpath('//*[@id="content-body"]/div/div[1]/div[1]/ul/li[2]/button')
        if not backupBtn.is_enabled(): 
            print('create backup button is not enable, please check if volume mounted onto vm.')
            return False
        backupBtn.click()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[2]/div/input').send_keys(backupName)
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        return True
    
    def clearVolume(self):
        ''' clear volume '''
        driver = self.driver
        driver.get(self.plate + self.disk)
        sleep(2)

        trs = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录": 
            return True
        for tr in trs:
            tr.find_element_by_xpath(".//td[1]/label").click()
            sleep(0.5)
        else:
            driver.find_element_by_xpath('//*[@id="storage-disk-more-action"]').click()
            sleep(0.5)
            driver.find_element_by_xpath('//*[@id="content-body"]/div/div[1]/div[1]/ul/li[5]/button').click()
            sleep(0.5)
            driver.find_element_by_xpath('//*[@id="common-widget-messagebox-checkbox-ok"]').click()
            sleep(0.5)
            self.volList.clear()
            return True
    
    def mountBackupPolicy(self):
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()