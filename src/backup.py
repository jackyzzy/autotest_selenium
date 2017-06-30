# coding=utf-8
from selenium import webdriver
from time import sleep
import config

class Backup():
    ''' Backup test case
    >>> pp = "http://100.1.22.1"
        
    >>> policy = 'aaa'
    
    >>> bkp = Backup(pp)
    
    >>> bkp.login()
    
    >>> bkp.policyMountToVolume(policy)
    
    >>> bkp.logout()
    
    '''
    def __init__(self, plate):
        self.plate = plate
        self.host = config.host
        self.backupChainPage = config.backupChainPage
        self.backupPolicyPage = config.backupPolicyPage
        self.userName = config.userName
        self.passwd = config.passWD
        self.driver = webdriver.Chrome()
        self.chainList = self.getChainList()
        self.policyList = self.getPolicyList()
        
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

    def getPolicyList(self):
        ''' get pollicy list '''
        driver = webdriver.Chrome()
        driver.get(self.plate + self.backupPolicyPage)
        driver.delete_all_cookies()
        driver.refresh()

        ''' login '''
        driver.find_element_by_id("id_username").send_keys(self.userName)
        driver.find_element_by_id("id_password").send_keys(self.passwd)
        driver.find_element_by_id("loginBtn").click()
        sleep(0.5)
        driver.get(self.plate + self.backupPolicyPage)
        sleep(2)
        
        policyList = []
        tr = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if tr[0].text == "没有找到匹配的记录": 
            return policyList
        for td in tr:
            pName = td.find_element_by_xpath('.//td[2]/div').text
            policyList.append(pName) 
        driver.quit()
        return policyList
    
    def createPolicy(self, policyName, policyTime = None):
        ''' create backup policy '''
        assert policyName != None
        
        if policyName in self.policyList :
            return
        
        driver = self.driver
        driver.get(self.plate + self.backupPolicyPage)
        sleep(2)
        
        ''' click add policy '''
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[1]/button[1]').click()
        sleep(0.5)
        
        ''' input policy name '''
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[2]/div/input').send_keys(policyName)
        sleep(0.5)
        
        if policyTime == None:
            ''' no policy time give '''
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
            self.policyList.append(policyName)
            return
        
        defaultTime = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[3]/div/div/select/option').get_attribute('value')
        if defaultTime == policyTime:
            ''' policy time is current rand time '''
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
            self.policyList.append(policyName)
            return
        else:
            ''' select policy time and submit '''
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[3]/div/div/span').click()
            sleep(0.5)
            select = policyTime % 24 + 1
            driver.find_element_by_xpath('/html/body/div[6]/div/ul/li[%d]' %(select)).click()
            sleep(0.5)
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
            self.policyList.append(policyName)
            return
    
    def deletePolicy(self, policyName):
        ''' delet policy '''
        assert policyName != None and len(self.policyList) != 0
        assert policyName in self.policyList
        
        driver = self.driver
        driver.get(self.plate + self.backupPolicyPage)
        sleep(2)
        
        tr = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if tr[0].text == "没有找到匹配的记录": 
            print('policy list is empty')
            return False
        for td in tr:
            pName = td.find_element_by_xpath('.//td[2]/div').text
            if pName == policyName :
                td.click()
                sleep(0.5)
                break
        else:
            print('policy[%s] is not find in backup policy page' %(policyName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[1]/button[4]').click()
        sleep(1)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(5)
        self.policyList.remove(policyName)
        return True
    
    def policyMountToVolume(self, policyName):
        ''' mount policy onto volume, in policy page '''
        assert policyName != None and len(self.policyList) != 0
        
        if policyName not in self.policyList:
            print('policy[%s] is not in policy list' %(policyName))
            return False
        driver = self.driver
        driver.get(self.plate + self.backupPolicyPage)
        sleep(2)
        
        tr = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if tr[0].text == "没有找到匹配的记录": 
            print('policy list is empty')
            return False
        for td in tr:
            pName = td.find_element_by_xpath('.//td[2]/div').text
            if pName == policyName :
                td.click()
                sleep(0.5)
                break
        else:
            print('policy[%s] is not find in backup policy page' %(policyName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[1]/button[2]').click()
        sleep(0.5)
        
        ul = driver.find_elements_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/ul')
        lis = ul.find_elements_by_xpath('.//li')
        for li in lis:
            name = li.find_element_by_xpath('.//div').get_attribute('title')
            print(name)
        
    
    def getChainList(self):
        ''' get backup chain list '''
        driver = webdriver.Chrome()
        driver.get(self.plate + self.backupChainPage)
        driver.delete_all_cookies()
        driver.refresh()

        ''' login '''
        driver.find_element_by_id("id_username").send_keys(self.userName)
        driver.find_element_by_id("id_password").send_keys(self.passwd)
        driver.find_element_by_id("loginBtn").click()
        sleep(0.5)
        driver.get(self.plate + self.backupChainPage)
        sleep(2)
        
        policyList = []
        tr = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if tr[0].text == "没有找到匹配的记录": 
            return policyList
        for td in tr:
            volName = td.find_element_by_xpath('.//td[3]/div').text
            policyList.append(volName) 
        driver.quit()
        return policyList
    
    def chainMountPolicy(self):
        pass
    
    def deleteChain(self):
        pass
    
    def gotoBackupList(self):
        pass
    
    def addPoint(self):
        pass
    
    def deletePoint(self):
        pass
    
    def recoverPoint(self, allVolume = True):
        pass
    
    def deletePointList(self):
        pass
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()