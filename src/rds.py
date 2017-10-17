# coding=utf-8
from selenium import webdriver
from random import randint
from time import sleep
import envConfig

class RDS():
    ''' rds db test case
    >>> pp = "http://100.1.22.1"
    
    >>> db = RDS(pp)
    
    >>> db.login()
    
    >>> db.createRDS('aaa')
    'aaa'
    >>> sleep(200)
    
    >>> db.createRDS('bbb')
    'bbb'
    >>> sleep(200)
    
    >>> db.renameRDS('aaa', 'ccc')
    
    >>> sleep(10)
    
    >>> db.changePW('bbb', 'test12345')
    
    >>> sleep(10)
    
    >>> db.deleteRDS('bbb')
    
    >>> db.deleteRDS('ccc')
    
    >>> db.logout()
    
    '''
    def __init__(self, plate):
        self.plate = plate
        self.host = envConfig.host
        self.RDSPage = envConfig.RDSPage
        self.userName = envConfig.userName
        self.passwd = envConfig.passWD
        self.driver = webdriver.Chrome()
        self.RDSList = self.getRDSList()
        self.instanceCNT = randint(2,100)
        self.instanceBase = envConfig.instanceBase
        
    def login(self):
        ''' login '''
        driver = self.driver
        driver.get(self.plate)
        driver.delete_all_cookies()
        driver.refresh()
        sleep(2)
        
        driver.find_element_by_id("id_username").send_keys(self.userName)
        sleep(0.5)
        driver.find_element_by_id("id_password").send_keys(self.passwd)
        sleep(0.5)
        driver.find_element_by_id("loginBtn").click()
        sleep(1)

    def logout(self):
        driver = self.driver
        ''' clear env '''
        driver.quit()
    
    def getRDSList(self):
        ''' get instance list '''
        driver = self.driver
        driver.get(self.plate)
        driver.delete_all_cookies()
        driver.refresh()
        
        driver.find_element_by_id("id_username").send_keys(self.userName)
        sleep(0.5)
        driver.find_element_by_id("id_password").send_keys(self.passwd)
        sleep(0.5)
        driver.find_element_by_id("loginBtn").click()
        sleep(1)
        
        RDSList = []
        driver.get(self.plate + self.RDSPage)
        sleep(2)
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if len(trs) == 0 :
            return RDSList
        if trs[0].find_element_by_xpath('.//td').text == '没有找到匹配的记录':
            return RDSList
        for tr in trs:
            instanceName = tr.find_element_by_xpath('.//td[3]/div/a').text
            RDSList.append(instanceName)
            tr.find_element_by_xpath('.//td[1]').click()
            sleep(0.5)
        return RDSList
    
    def createRDS(self, rdsName = None, instancePW = 'admin123'):
        driver = self.driver
        driver.get(self.plate + self.RDSPage)
        sleep(2)
        
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div/div/div[1]/div/button[1]').click()
        sleep(1)
        
        # select level
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div/form/div[3]/ul/li/div[2]/span').click()
        sleep(1)
#         driver.find_element_by_css_selector('[data-value="datastore.8c16384m"]').click()
        driver.find_element_by_css_selector('[data-idx="2"]').click()
        sleep(1)
        
        # input volume size 
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div/form/div[5]/ul/li/input').clear()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div/form/div[5]/ul/li/input').send_keys('20')
        sleep(1)
        
        # select sub net
        #TODO: if no sub net, create one;
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div/form/div[7]/ul/li[1]/div[2]/span').click()
        sleep(1)
        driver.find_element_by_xpath('/html/body/div[7]/div/ul/li').click()
        sleep(1)
        
        # click next
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[2]').click()
        sleep(1)
                
        # input instance name
        if not rdsName:
            rdsName = self.instanceBase + str(self.instanceCNT)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[2]/form/div[1]/div/input').clear()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[2]/form/div[1]/div/input').send_keys(rdsName)
        sleep(0.5)
        
        # input password
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[2]/form/div[3]/div/input[2]').clear()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[2]/form/div[3]/div/input[2]').send_keys(instancePW)
        sleep(0.5)
        
        # conform password
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[2]/form/div[4]/div/input[2]').clear()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[2]/form/div[4]/div/input[2]').send_keys(instancePW)
        sleep(0.5)
        
        # submit create
        if not driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[2]').is_enabled():
            print("fail to create RDS instanc[%s]" % (rdsName))
            return False

        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[2]').click()
        sleep(0.5)
        clos = driver.find_elements_by_class_name('bootstrap-dialog-footer-buttons')
        for clo in clos:
            bts = clo.find_elements_by_xpath('.//button')
            if len(bts) != 1:
                continue
            if not bts[0].text == '关闭':
                continue
            if bts[0].is_enabled():
                print("fail to create RDS instance[%s], no quota left" %(rdsName))            
                return False
        else:
            self.RDSList.append(rdsName)
            self.instanceCNT = self.instanceCNT + 1
            return rdsName
        
    def deleteRDS(self, instanceName):
        driver = self.driver
        driver.get(self.plate + self.RDSPage)
        sleep(2)
        
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        for tr in trs:
            name = tr.find_element_by_xpath('.//td[3]/div/a').text
            if name != instanceName:
                continue
            tr.find_element_by_xpath('.//td[1]').click()
            sleep(1)
            break
        else:
            print("no RDS instance [%s] finded, in RDS list" %(instanceName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div/div/div[1]/div/button[4]').click()
        sleep(1)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        self.RDSList.remove(instanceName)
            
    def renameRDS(self, RDSName, newName):
        driver = self.driver
        driver.get(self.plate + self.RDSPage)
        sleep(2)
        
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        for tr in trs:
            name = tr.find_element_by_xpath('.//td[3]/div/a').text
            if name != RDSName:
                continue
            tr.find_element_by_xpath('.//td[1]').click()
            sleep(1)
            break
        else:
            print("no RDS instance [%s] finded, in RDS list" %(RDSName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div/div/div[1]/div/button[3]').click()
        sleep(1)
                            
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div/div/input').clear()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div/div/input').send_keys(newName)
        sleep(1)

        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        self.RDSList.remove(RDSName)
        self.RDSList.append(newName)
    
    def changePW(self, RDSName, newPW):
        driver = self.driver
        driver.get(self.plate + self.RDSPage)
        sleep(2)
        
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        for tr in trs:
            name = tr.find_element_by_xpath('.//td[3]/div/a').text
            if name != RDSName:
                continue
            tr.find_element_by_xpath('.//td[1]').click()
            sleep(1)
            break
        else:
            print("no RDS instance [%s] finded, in RDS list" %(RDSName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div/div/div[1]/div/button[2]').click()
        sleep(1)
        
        
        fm = driver.find_element_by_class_name('dialog-vertical-container')
        fm.find_element_by_xpath('.//div[2]/div/div[2]/div[1]/div/form/div[1]/div/input').clear()
        sleep(0.5)
        fm.find_element_by_xpath('.//div[2]/div/div[2]/div[1]/div/form/div[1]/div/input').send_keys(newPW)
        sleep(1)
        
        fm.find_element_by_xpath('.//div[2]/div/div[2]/div[1]/div/form/div[2]/div/input').clear()
        sleep(0.5)
        fm.find_element_by_xpath('.//div[2]/div/div[2]/div[1]/div/form/div[2]/div/input').send_keys(newPW)
        sleep(1)
        
#         driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[1]/div/input').clear()
#         sleep(0.5)
#         driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[1]/div/input').send_keys(newPW)
#         sleep(1)
#         
#         driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[2]/div/input').clear()
#         sleep(0.5)
#         driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[2]/div/input').send_keys(newPW)
#         sleep(1)
        
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
    
    def clearRDS(self):
        driver = self.driver
        driver.get(self.plate + self.RDSPage)
        sleep(2)
        
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div[2]/table/thead/tr/th[1]/div[1]/label').click()
        sleep(1)   
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div/div/div[1]/div/button[4]').click()
        sleep(1)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        self.RDSList.clear()   

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    