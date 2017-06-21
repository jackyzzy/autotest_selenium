# coding=utf-8
from selenium import webdriver
from time import sleep
from random import randint
from selenium.common import exceptions as SEE
import pip
import check
import config
import volume

class Instance():
    '''
    >>> pp = "http://100.86.0.1"
            
    >>> inc = Instance(pp) 
                
    >>> inc.login()
    
    >>> vm = inc.createInstance('bbb')
    bbb
    >>> sleep(60)
    
    >>> inc.connect(vm)
    public ip connected !
    True
    >>> sleep(3)
    
    >>> inc.shutdownOuter(vm)
    True
    >>> sleep(100)
    
    >>> inc.mountVolume(vm, 'vvv1')
    True
    >>> sleep(10)
    
    >>> inc.mountVolume(vm, 'vvv a')
    True
    >>> sleep(10)
    
    >>> inc.startInstance(vm)
    True
    >>> sleep(100)
    
    >>> inc.connect(vm)
    public ip connected !
    True
    >>> inc.createBackup(vm, True)
    True
    >>> sleep(20)
    
    >>> inc.shutdownOuter(vm)
    True
    >>> sleep(60)
    
    >>> inc.umountVolume(vm, 'vvv1')
    True
    >>> sleep(10)
    
    >>> inc.umountVolume(vm, 'vvv a')
    True
    >>> sleep(10)
    
    >>> inc.startInstance(vm)
    True
    >>> sleep(60)
    
    >>> inc.restartOuter(vm)
    True
    >>> sleep(100)
    
    >>> inc.connect(vm)
    public ip connected !
    True
    >>> sleep(3)
    
    >>> inc.shutdownInner(vm)
    shutdown -h 0
    b''
    True
    >>> sleep(300)
    
    >>> inc.startInstance(vm)
    True
    >>> sleep(100)
    
    >>> inc.connect(vm)
    public ip connected !
    True
    >>> inc.restartInner(vm)
    True
    >>> sleep(300)
    
    >>> inc.connect(vm)
    public ip connected !
    True
    >>> inc.deleteInstance(vm)
    True
    >>> inc.logout()
        
    '''
    def __init__(self, plate):
        self.plate = plate
        self.host = config.host
        self.disk = config.disk
        self.userName = config.userName
        self.passWD = config.passWD
        self.vmbase = config.vmBase
        self.vmpw = config.vmPWD
        self.vmcnt = randint(2,100)
        self.check = check.Check()
        self.vmlist = self.getInstanceList()
        self.driver = webdriver.Chrome()

    def login(self):
        driver = self.driver
        driver.get(self.plate)
        driver.delete_all_cookies()
        driver.refresh()
        
        ''' login '''
        driver.find_element_by_id("id_username").send_keys(self.userName)
        driver.find_element_by_id("id_password").send_keys(self.passWD)
        driver.find_element_by_id("loginBtn").click()
        sleep(0.5)

    def logout(self):
        driver = self.driver
        driver.quit()
      
    def getInstanceList(self):
        ''' get instance list '''
        driver = webdriver.Chrome()
        vmList = []
        
        driver.get(self.plate)
        driver.delete_all_cookies()
        driver.refresh()
        
        ''' login '''
        driver.find_element_by_id("id_username").send_keys("zzy@sangfor.com")
        driver.find_element_by_id("id_password").send_keys("Admin12345")
        driver.find_element_by_id("loginBtn").click()
        sleep(0.5)
        
        driver.get(self.plate + self.host)
        sleep(2)
        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        if rd[0].text == "没有找到匹配的记录":
            return vmList
        for td in rd:
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            vmList.append(instanceName)
        driver.quit()
        return vmList
    
    def createInstance(self, vmName = None):
        ''' create instance '''
        driver = self.driver
        
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
        if not vmName:
            vmName = self.vmbase+str(self.vmcnt)
        name.clear()
        name.send_keys(vmName)
        pw = driver.find_element_by_xpath('html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[4]/form/div[5]/div/input[2]')
        pw.clear()
        pw.send_keys(self.vmpw)
        rpw = driver.find_element_by_xpath('html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[4]/form/div[6]/div/input[2]')
        rpw.clear()
        rpw.send_keys(self.vmpw)
        sleep(0.5)
        driver.find_element_by_xpath('html/body/div[5]/div/div[2]/div/div[3]/div/div/button[2]').click()
        sleep(10)
        self.vmlist.append(vmName)
        self.vmcnt = self.vmcnt + 1
        print(vmName)
        return vmName
    
    def deleteInstance(self, vmName):
        ''' delete instance '''
        assert len(self.vmlist) != 0
        assert vmName != None and vmName in self.vmlist
        
        driver = self.driver
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        if rd[0].text == "没有找到匹配的记录":
            print('instance list is empty')
            return False
        for td in rd:
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            if instanceName != vmName:
                continue
            td.find_element_by_xpath(".//td[1]/label").click()
            sleep(0.5)
            break
        else:
            print('vm[%s] is not find in instance page' %(vmName))
            return False
        driver.find_element_by_xpath('//*[@id="host-btn-more-computer"]').click()
        sleep(0.5)
        driver.find_element_by_xpath('//*[@id="content-body"]/div/div[2]/div[1]/div[1]/ul/li[8]/button').click()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        self.vmlist.remove(vmName)
        return True
            
    def connect(self, vmName):
        ''' connect to vm '''
        assert len(self.vmlist) != 0
        assert vmName in self.vmlist
        
        driver = self.driver
        driver.get(self.plate + self.host)
        sleep(2)
        
        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        if rd[0].text == "没有找到匹配的记录":
            print('instance list is empty')
            return False
        for td in rd:
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            if instanceName != vmName:
                continue
            status = td.find_element_by_xpath('.//td[2]/span').get_attribute('title')
            if status != '运行中' :
                return False
            try : 
                pip = td.find_element_by_xpath('.//td[11]/div').text
            except SEE.NoSuchElementException :
                print('vm[%s] has no public ip' %(vmName))
                return False
            iip = td.find_element_by_xpath('.//td[10]/div').text
            if self.check.check_ip(pip, 22, 'root', self.vmpw, iip):
                print("public ip connected !")
                return True
            else :
                img = td.find_element_by_xpath('.//td[5]/div').text
                print("public ip not connected !")
                print(status.get_attribute('title'))
                print(instanceName.text)
                print(img)
                print(iip)
                print(pip)
                return False
            break
        else:
            print('vm[%s] is not find in instance page' %(vmName))
            return False
    
    def getInstanceStatus(self, vmname):
        ''' get instance status '''
        assert len(self.vmlist) != 0
        assert vmname in self.vmlist
        
        driver = self.driver
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        if rd[0].text == "没有找到匹配的记录":
            return None
        for td in rd:
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            if instanceName != vmname:
                continue
            status = td.find_element_by_xpath('.//td[2]/span').get_attribute('title')
            return status
        else:
            return None
    
    def shutdownInner(self, vmName):
        ''' shutdown instance inner '''
        assert len(self.vmlist) != 0
        assert vmName in self.vmlist
        
        driver = self.driver
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        if rd[0].text == "没有找到匹配的记录":
            print('instance list is empty')
            return False
        for td in rd:
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            if instanceName != vmName:
                continue
            status = td.find_element_by_xpath('.//td[2]/span').get_attribute('title')
            if status != '运行中' :
                return False
            try : 
                pip = td.find_element_by_xpath('.//td[11]/div').text
            except SEE.NoSuchElementException :
                print('vm[%s] has no public ip' %(vmName))
                return False
            return self.check.shutdown_inner(pip, 22, 'root', self.vmpw)
        else:
            print('vm[%s] is not find in instance page' %(vmName))
            return False
    
    def shutdownOuter(self, vmName):
        ''' shutdown instance outer '''
        assert len(self.vmlist) != 0
        assert vmName in self.vmlist
        
        driver = self.driver
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        if rd[0].text == "没有找到匹配的记录":
            print('instance list is empty')
            return False
        for td in rd:
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            if instanceName != vmName:
                continue
            status = td.find_element_by_xpath('.//td[2]/span').get_attribute('title')
            if status != '运行中' and status != '正在备份':
                print('vm[%s] is not running or backup, status is %s' %(instanceName, status))
                return False
            td.click()
            sleep(0.5)
            break
        else:
            print('vm[%s] is not find in instance page' %(vmName))
            return False
        driver.find_element_by_xpath('//*[@id="host-btn-shutdown-computer"]').click()
        sleep(1)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        return True
    
    def shutdownOuterForce(self, vmName):
        ''' shutdown instance outer '''
        assert len(self.vmlist) != 0
        assert vmName in self.vmlist
        
        driver = self.driver
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        if rd[0].text == "没有找到匹配的记录":
            print('instance list is empty')
            return False
        for td in rd:
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            if instanceName != vmName:
                continue
            status = td.find_element_by_xpath('.//td[2]/span').get_attribute('title')
            if status != '运行中' :
                print('vm[%s] is not in running' %(instanceName))
                return False        
            td.click()
            sleep(0.5)
            break
        else:
            print('vm[%s] is not find in instance page' %(vmName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/button').click()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/ul/li[2]/button').click()
        sleep(1)
        return True
    
    def startInstance(self, vmName):
        ''' start instance in page '''
        assert len(self.vmlist) != 0
        assert vmName != None and vmName in self.vmlist
        
        driver = self.driver
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        if rd[0].text == "没有找到匹配的记录":
            print('instance list is empty')
            return False
        for td in rd:
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            if instanceName != vmName:
                continue
            status = td.find_element_by_xpath('.//td[2]/span').get_attribute('title')
            if status != '已关机':
                print('vm[%s] is not in shutdown' %(instanceName))
                return False
            td.click()
            sleep(0.5)
            break
        else:
            print('vm[%s] is not find in instance page' %(vmName))
            return False    
        driver.find_element_by_xpath('//*[@id="host-btn-start-computer"]').click()
        sleep(2)
        return True
        
    
    def restartInner(self, vmName):
        ''' restart instance inner '''
        assert len(self.vmlist) != 0
        assert vmName in self.vmlist
        
        driver = self.driver
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        if rd[0].text == "没有找到匹配的记录":
            print('instance list is empty')
            return False
        for td in rd:
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            if instanceName != vmName:
                continue
            status = td.find_element_by_xpath('.//td[2]/span').get_attribute('title')
            if status != '运行中' :
                print('vm[%s] is not in running' %(instanceName))
                return False
            try : 
                pip = td.find_element_by_xpath('.//td[11]/div').text
            except SEE.NoSuchElementException :
                print('vm[%s] has no public ip' %(vmName))
                return False
            return self.check.restart_inner(pip, 22, 'root', self.vmpw)
        else:
            print('vm[%s] is not find in instance page' %(vmName))
            return False
    
    def restartOuter(self, vmName):
        ''' restart instance outer '''
        assert len(self.vmlist) != 0
        assert vmName in self.vmlist
        
        driver = self.driver
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        if rd[0].text == "没有找到匹配的记录":
            print('instance list is empty')
            return False
        for td in rd:
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            if instanceName != vmName:
                continue
            status = td.find_element_by_xpath('.//td[2]/span').get_attribute('title')
            if status != '运行中' :
                return False
            td.click()
            sleep(0.5)
            break
        else:
            print('vm[%s] is not find in instance page' %(vmName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/button').click()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/ul/li[1]/button').click()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        return True
    
    def createBackup(self, vmName, backupName, allVolume = True):
        ''' instance create backup '''
        assert len(self.vmlist) != 0
        assert vmName in self.vmlist
        
        driver = self.driver
        driver.get(self.plate + self.host)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        if rd[0].text == "没有找到匹配的记录":
            print('instance list is empty')
            return False
        for td in rd:
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            if instanceName != vmName:
                continue
            status = td.find_element_by_xpath('.//td[2]/span').get_attribute('title')
            if status != '运行中'  and  status != '已关机':
                print('vm[%s] status error, not 运行中   or 已关机' %(instanceName))
                return False
            td.click()
            sleep(0.5)
            break
        else:
            print('vm[%s] is not find in instance page' %(vmName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/button[5]').click()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[2]/div/input').send_keys(backupName)
        sleep(0.5)
        if allVolume:
            volumes = driver.find_elements_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[3]/div/div')
            volumes.pop(0)
            for vol in volumes:
                vol.find_element_by_xpath('.//label').click()
                sleep(0.5)                
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        return True
        
    def mountVolume(self, vmName, volName):
        ''' mount volume to instance '''
        assert len(self.vmlist) != 0
        assert vmName in self.vmlist
        
        driver = self.driver
        driver.get(self.plate + self.host)
        sleep(2)

        vol = volume.Volume(self.plate)
        vol.login()
        volStatus = vol.getVolumeStatus(volName)
        if volStatus != '未挂载':
            print('volume[%s] is in use, status is %s.' %(volName, volStatus))
            vol.logout()
            return False
        vol.logout
        
        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        if rd[0].text == "没有找到匹配的记录":
            print('instance list is empty')
            return False
        for td in rd:
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            if instanceName != vmName:
                continue
            status = td.find_element_by_xpath('.//td[2]/span').get_attribute('title')
            if status != '已关机':
                print('vm[%s] is not turned off' %(instanceName))
                return False
            td.click()
            sleep(0.5)
            break
        else:
            print('vm[%s] is not find in instance page' %(vmName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/button').click()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/ul/li[5]/button').click()
        sleep(0.5)
        ul = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div/div[1]/table/tbody/tr[2]/td[1]/ul')
        try:
            vols = ul.find_elements_by_xpath('.//li[@class="ellipsis"]')
            for vv in vols:
                ss = vv.text
                if ss.find(volName) == 0 and ss[len(volName)] == ' ' and ss[len(volName) + 1] == '（':
                    vv.click()
                    sleep(0.5)
                    break
            else:
                print('volume[%s] is not find' %(volName))
                return False
        except SEE.NoSuchElementException :
            print('no vol availabe to mounte to vm[%s]' %(vmName))
            return False
        
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div/div[1]/table/tbody/tr[2]/td[2]/button[1]').click()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        return True
    
    def umountVolume(self, vmName, volName):
        ''' umount volume from instance '''
        assert len(self.vmlist) != 0
        assert vmName in self.vmlist
        
        driver = self.driver
        driver.get(self.plate + self.host)
        sleep(3)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        if rd[0].text == "没有找到匹配的记录":
            print('instance list is empty')
            return False
        for td in rd:
            instanceName = td.find_element_by_xpath('.//td[3]/div').text
            if instanceName != vmName:
                continue
            status = td.find_element_by_xpath('.//td[2]/span').get_attribute('title')
            if status != '已关机' :
                print('vm[%s] is still running' %(vmName))
                return False
            
            td.click()
            sleep(0.5)
            break
        else:
            print('vm[%s] is not find in instance page' %(vmName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/button').click()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/ul/li[6]/button').click()
        sleep(0.5)
        
        ul = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div/div[2]/ul')
        try:
            vols = ul.find_elements_by_xpath('.//li')
            for vol in vols:
                ss = vol.text
                if ss.find(volName) == 0 and ss[len(volName)] == ' ' and ss[len(volName) + 1] == '（' and ss[len(volName) + 2] == '容':
                    vol.click()
                    sleep(0.5)
                    break
            else:
                print('vol[%s] not find on %s' %(volName, vmName))
                return False
        except SEE.NoSuchElementException :
            print('no volume mounted on %s' %(vmName))
            return False
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        return True
    
    def configPublicIP(self):
        ''' config public ip into instance '''
        #TODO: fix me
        pass
    
    def configSubNet(self):
        ''' config sub net into instance '''
        #TODO: fix me
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
