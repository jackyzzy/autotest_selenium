# coding=utf-8
from selenium import webdriver
from time import sleep
from random import randint
from selenium.common import exceptions as SEE
import pip
import check
import config

class Instance():
    '''
    >>> pp = "http://100.86.0.1"
    
    >>> vm = 'aaa'
        
    >>> inc = Instance(pp) 
                
    >>> inc.login()
    
    >>> inc.shutdownOuter(vm)
    True
    >>> sleep(30)
    
    >>> inc.startInstance(vm)
    True
    >>> sleep(60)
    
    >>> inc.restartInstanceOuter(vm)
    True
    >>> sleep(30)
    
    >>> inc.shutdownOuterForce(vm)
    True
    >>> inc.logout()
        
    '''
    def __init__(self, plate):
        self.plate = plate
        self.host = config.host
        self.disk = config.disk
        self.vmbase = config.vmbase
        self.vmpw = config.vmpw
        self.vmcnt = randint(2,100)
        self.check = check.Check()
        self.vmlist = self.getInstanceList()
#         self.driver = webdriver.Edge()
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
#         sleep(3)
        driver.quit()
      
    def getInstanceList(self):
        ''' 
        get instance list 
        '''
        driver = webdriver.Chrome()       
        driver.get(self.plate)
        driver.delete_all_cookies()
        driver.refresh()
        
        ''' login '''
        driver.find_element_by_id("id_username").send_keys("zzy@sangfor.com")
        driver.find_element_by_id("id_password").send_keys("Admin12345")
        driver.find_element_by_id("loginBtn").click()
        sleep(0.5)
        
        # go to plate page
        driver.get(self.plate + self.host)
        sleep(2)
        vmList = []
        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return vmList
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            vmList.append(instanceName)
        driver.quit()
        return vmList
    
    def createInstance(self):
        '''
        create instance
        '''
        
        driver = self.driver
        # go to plate page
        driver.get(self.plate + self.host)
        sleep(2)
        
        ''' click new instance '''
#         driver.find_element_by_id("plate-btn-create-computer").click()  
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/button[1]').click()
        sleep(1)
        
        ''' select image '''
        driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div[3]/ul/li[1]/div").click()
#         driver.find_element_by_xpath("//*[@class='plate-add-image-detail-panel plate-add-image-common-panel']/ul/li[1]/div").click()
        
        ''' click next after image '''
        driver.find_element_by_xpath("//*[@class='btn btn-primary btn-submit']").click()
#         driver.find_element_by_xpath("//*[@id='site-my-list']/ul/li[2]/div").click()
        
        ''' click next after configuration '''
        driver.find_element_by_xpath('html/body/div[5]/div/div[2]/div/div[3]/div/div/button[2]').click()
        # click next after networking
        driver.find_element_by_xpath('html/body/div[5]/div/div[2]/div/div[3]/div/div/button[2]').click()
        
        ''' click go after base inrormation: instance name, pw '''
        name = driver.find_element_by_xpath('//input[@class="form-control" and @name="name" and @data-fv-field="name" and @type="text"]')
        vmname = self.vmbase+str(self.vmcnt)
        name.clear()
        name.send_keys(vmname)
        pw = driver.find_element_by_xpath('html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[4]/form/div[5]/div/input[2]')
        pw.clear()
        pw.send_keys(self.vmpw)
        rpw = driver.find_element_by_xpath('html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[4]/form/div[6]/div/input[2]')
        rpw.clear()
        create = driver.find_element_by_xpath('html/body/div[5]/div/div[2]/div/div[3]/div/div/button[2]')
        if create.is_enabled() == True:
            print("before, enable")
        else:
            print("before, not enable")
        rpw.send_keys(self.vmpw)
        sleep(1)
        if create.is_enabled() == True:
            print("after, enable")
        else:
            print("after, not enable")
        create.click()
        sleep(10)
        self.vmlist.append(vmname)
        self.vmcnt = self.vmcnt + 1
        print(self.vmlist)
        return vmname
    
    def deleteInstance(self, vmname):
        ''' 
        delete instance 
        '''
        assert len(self.vmlist) != 0
        assert vmname in self.vmlist
        
        driver = self.driver
        # go to plate page
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return
            
            checkLable = td.find_element_by_xpath(".//td[1]/label")
            inc = td.find_element_by_xpath('.//td[3]/div')
            if vmname != None and inc.text != vmname:
                continue
            
            checkLable.click()
            driver.find_element_by_xpath('//*[@id="host-btn-more-computer"]').click()
            sleep(0.5)
            driver.find_element_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[1]/ul/li[8]/button').click()
            sleep(1)
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        
        self.vmlist.remove(vmname)
        sleep(5)
            
    def connect(self, vmname):
        '''
        test the unicom of vm public ip
        '''
        assert len(self.vmlist) != 0
        assert vmname in self.vmlist
        
        driver = self.driver
        # go to plate page
        driver.get(self.plate + self.host)
        sleep(2)
        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return False
            
            status = td.find_element_by_xpath('.//td[2]/span')
            instanceName = td.find_element_by_xpath('.//td[3]/div')
            img = td.find_element_by_xpath('.//td[5]/div').text
            iip = td.find_element_by_xpath('.//td[10]/div').text
            if instanceName.text != vmname:
                continue
            if status.get_attribute('title') != '运行中' :
                return False
            try : 
                pip = td.find_element_by_xpath('.//td[11]/div').text
            except SEE.NoSuchElementException :
                print('vm[%s] has no public ip' %(vmname))
                return False
            
            if self.check.check_ip(pip, 22, 'root', self.vmpw, iip):
                print("public ip connected !")
                return True
            else :
                print("public ip not connected !")
                print(status.get_attribute('title'))
                print(instanceName.text)
                print(img)
                print(iip)
                print(pip)
                return False
    
    def getInstanceStatus(self, vmname):
        ''' 
        get instance status 
        '''
        assert len(self.vmlist) != 0
        assert vmname in self.vmlist
        
        driver = self.driver
        # go to plate page
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return None
            
            status = td.find_element_by_xpath('.//td[2]/span').get_attribute('title')
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            
            if instanceName != vmname:
                continue
            
            return status
        return None
    
    def shutdownInner(self, vmname):
        ''' 
        shutdown instance inner
        '''
        assert len(self.vmlist) != 0
        assert vmname in self.vmlist
        
        driver = self.driver
        # go to plate page
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return False
            
            status = td.find_element_by_xpath('.//td[2]/span')
            instanceName = td.find_element_by_xpath('.//td[3]/div')
            if instanceName.text != vmname:
                continue
            if status.get_attribute('title') != '运行中' :
                return False
            try : 
                pip = td.find_element_by_xpath('.//td[11]/div').text
            except SEE.NoSuchElementException :
                print('vm[%s] has no public ip' %(vmname))
                return False
            if self.check.shutdown_inner(pip, 22, 'root', self.vmpw) == False:
                return False
            return True
        return False
    
    def shutdownOuter(self, vmname):
        ''' 
        shutdown instance outer
        '''
        assert len(self.vmlist) != 0
        assert vmname in self.vmlist
        
        driver = self.driver
        # go to plate page
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                print('there is no vm')
                return False
            
            instanceName = td.find_element_by_xpath('.//td[3]/div')
            if instanceName.text != vmname:
                continue
            status = td.find_element_by_xpath('.//td[2]/span').get_attribute('title')
            if status != '运行中' :
                print('vm[%s] is still running' %(instanceName))
                return False
            
            td.click()
            sleep(0.5)
            driver.find_element_by_xpath('//*[@id="host-btn-shutdown-computer"]').click()
            sleep(1)
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
            sleep(3)
            return True
        print('vm[%s] is not find' %(vmname))
        return False
    
    def shutdownOuterForce(self, vmName):
        ''' 
        shutdown instance outer
        '''
        assert len(self.vmlist) != 0
        assert vmName in self.vmlist
        
        driver = self.driver
        # go to plate page
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return False
            
            status = td.find_element_by_xpath('.//td[2]/span')
            instanceName = td.find_element_by_xpath('.//td[3]/div')
            if instanceName.text != vmName:
                continue
            if status.get_attribute('title') != '运行中' :
                return False
            
            td.click()
            sleep(0.5)
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/button').click()
            sleep(0.5)
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/ul/li[2]/button').click()
            sleep(1)
            return True
    
    def startInstance(self, vmname):
        ''' 
        start instance in page        
        '''
        assert len(self.vmlist) != 0
        assert vmname != None
        assert vmname in self.vmlist
        
        driver = self.driver
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                print ('no instance')
                return False
            
            status = td.find_element_by_xpath('.//td[2]/span')
            inc = td.find_element_by_xpath('.//td[3]/div')
            if vmname != None and inc.text != vmname:
                continue
            
            if status.get_attribute('title') != '已关机':
                print('no close')
                return False
            
            td.click()
            sleep(0.5)
            driver.find_element_by_xpath('//*[@id="host-btn-start-computer"]').click()
            sleep(2)
            return True
        
        print ('no match')
        return False
    
    def restartInstanceInner(self, vmname):
        ''' 
        restart instance inner 
        '''
        assert len(self.vmlist) != 0
        assert vmname in self.vmlist
        
        driver = self.driver
        # go to plate page
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return False
            
            status = td.find_element_by_xpath('.//td[2]/span')
            instanceName = td.find_element_by_xpath('.//td[3]/div')
            if instanceName.text != vmname:
                continue
            if status.get_attribute('title') != '运行中' :
                return False
            try : 
                pip = td.find_element_by_xpath('.//td[11]/div').text
            except SEE.NoSuchElementException :
                print('vm[%s] has no public ip' %(vmname))
                return False
            if self.check.restart_inner(pip, 22, 'root', self.vmpw) == False:
                return False
            return True
        return False
    
    def restartInstanceOuter(self, vmname):
        ''' 
        restart instance outer
        '''
        assert len(self.vmlist) != 0
        assert vmname in self.vmlist
        
        driver = self.driver
        # go to plate page
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return False
            
            status = td.find_element_by_xpath('.//td[2]/span')
            instanceName = td.find_element_by_xpath('.//td[3]/div')
            if instanceName.text != vmname:
                continue
            if status.get_attribute('title') != '运行中' :
                return False
            
            td.click()
            sleep(0.5)
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/button').click()
            sleep(0.5)
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/ul/li[1]/button').click()
            sleep(1)
            return True
        
        return False
    
    def createBackup(self):
        #TODO: fix me
        pass
    
    def mountVolume(self):
        #TODO: fix me
        pass
    
    def umountVolume(self):
        #TODO: fix me
        pass
    
    def configPublicIP(self):
        #TODO: fix me
        pass
    
    def configSubNet(self):
        #TODO: fix me
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
