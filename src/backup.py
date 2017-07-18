# coding=utf-8
from selenium import webdriver
from time import sleep
import envConfig

class Backup():
    ''' Backup test case
    >>> pp = "http://100.1.22.1"
        
    >>> policy = 'aaa'
    
    >>> bkp = Backup(pp)
    
    >>> bkp.login()
    
    >>> bkp.clearBackupChain()
    True
    >>> bkp.clearBackupPolicy()
    True
    >>> sleep(10)
    
    >>> bkp.logout()
    
    '''
    def __init__(self, plate):
        self.plate = plate
        self.host = envConfig.host
        self.backupChainPage = envConfig.backupChainPage
        self.backupPolicyPage = envConfig.backupPolicyPage
        self.userName = envConfig.userName
        self.passwd = envConfig.passWD
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

    def clearBackupChain(self):
        ''' clear backup chain '''
        driver = self.driver
        driver.get(self.plate + self.backupChainPage)
        sleep(2)
        
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录":
            return True
        for tr in trs:
            tr.find_element_by_xpath('.//td[1]/label').click()
            sleep(0.5)
        else:
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/div/div[1]/button[2]').click()
            sleep(0.5)
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
            sleep(0.5)
            self.chainList.clear()
            return True
        
    def clearBackupPolicy(self):
        ''' clear policy '''
        driver = self.driver
        driver.get(self.plate + self.backupPolicyPage)
        sleep(2)
        
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录":
            return True
        for tr in trs:
            tr.find_element_by_xpath('.//td[1]/label').click()
            sleep(0.5)
        else:
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[1]/button[4]').click()
            sleep(0.5)
            driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
            sleep(0.5)
            self.policyList.clear()
            return True

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
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录": 
            return policyList
        for tr in trs:
            pName = tr.find_element_by_xpath('.//td[2]/div').text
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
        
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录": 
            print('policy list is empty')
            return False
        for tr in trs:
            pName = tr.find_element_by_xpath('.//td[2]/div').text
            if pName == policyName :
                tr.click()
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
    
    def policyMountToVolume(self, policyName, volName, volType, allVol = False):
        ''' mount policy onto volume, in policy page '''
        assert policyName != None and len(self.policyList) != 0
        
        if policyName not in self.policyList:
            print('policy[%s] is not in policy list' %(policyName))
            return False
        driver = self.driver
        driver.get(self.plate + self.backupPolicyPage)
        sleep(2)
        
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录": 
            print('policy list is empty')
            return False
        for tr in trs:
            pName = tr.find_element_by_xpath('.//td[2]/div').text
            if pName == policyName :
                tr.click()
                sleep(0.5)
                break
        else:
            print('policy[%s] is not find in backup policy page' %(policyName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[1]/button[2]').click()
        sleep(0.5)
        
        if allVol:
            driver.find_element_by_class_name('backup-disk-select-all').click()
            sleep(0.5)
            driver.find_element_by_xpath("//button[contains(@class,'btn btn-submit btn-primary')]").click()
            sleep(1)
            return True
        
        groups = driver.find_elements_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/ul/li')
        for group in groups:
            ul = group.find_element_by_xpath('.//ul')
            lis = ul.find_elements_by_xpath('.//li')
            for li in lis:
                diskName = li.find_element_by_xpath('.//div/span[2]').text
                vol = "%s：%s" %(volType, volName)
                if vol  != diskName:
                    continue
                li.find_element_by_xpath('.//div/label').click()
                driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
                sleep(1)
                return True
        else:
            print('volume[%s：%s] is not find in the volume list' %(volType, volName))
            return False
    
    def policyUMountAll(self, policyName):
        ''' mount policy onto volume, in policy page '''
        assert policyName != None and len(self.policyList) != 0
        
        if policyName not in self.policyList:
            print('policy[%s] is not in policy list' %(policyName))
            return False
        driver = self.driver
        driver.get(self.plate + self.backupPolicyPage)
        sleep(2)
        
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录": 
            print('policy list is empty')
            return False
        for tr in trs:
            pName = tr.find_element_by_xpath('.//td[2]/div').text
            if pName == policyName :
                tr.click()
                sleep(0.5)
                break
        else:
            print('policy[%s] is not find in backup policy page' %(policyName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[1]/button[2]').click()
        sleep(0.5)    
        select = driver.find_element_by_class_name('backup-disk-select-all')
        if select.text == '全选':
            select.click()
            sleep(0.5)
            select.click()
            sleep(0.5)
        elif select.text == '清空':
            select.click()
            sleep(0.5)
        driver.find_element_by_xpath("//button[contains(@class,'btn btn-submit btn-primary')]").click()
        sleep(1)
        return True
    
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
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录": 
            return policyList
        for tr in trs:
            volName = tr.find_element_by_xpath('.//td[3]/div').text
            policyList.append(volName) 
        driver.quit()
        return policyList
    
    def chainMountPolicy(self, chainName, policyName):
        ''' chain mount to policy '''
        assert chainName != None and policyName != None and len(self.chainList) != 0 and len(self.policyList) != 0
        assert chainName in self.chainList
        assert policyName in self.policyList
        
        driver = self.driver
        driver.get(self.plate + self.backupChainPage)
        sleep(2)
        
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录": 
            print('chain list is empty')
            return False
        for tr in trs:
            volName = tr.find_element_by_xpath('.//td[3]/div').text
            if volName == chainName :
                tr.click()
                sleep(0.5)
                break
        else:
            print('chain[%s] is not find in backup chain page' %(chainName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/div/div[1]/button[1]').click()
        sleep(0.5)
        driver.find_element_by_xpath('//*[@id="fixselect-1"]/span').click()
        sleep(0.5)
        policyList = driver.find_elements_by_xpath('/html/body/div[6]/div/ul/li')
        for policy in policyList:
            if policy.text == policyName:
                policy.click()
                sleep(0.5)
                break
        else:
            print('policy list is empty')
            return False
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(0.5)
        return True
    
    def deleteChain(self, chainName):
        ''' delet backup chain '''
        assert chainName != None and len(self.chainList) != 0
        assert chainName in self.chainList
        
        driver = self.driver
        driver.get(self.plate + self.backupChainPage)
        sleep(2)
        
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录": 
            print('chain list is empty')
            return False
        for tr in trs:
            volName = tr.find_element_by_xpath('.//td[3]/div').text
            if volName == chainName :
                tr.click()
                sleep(0.5)
                break
        else:
            print('chain[%s] is not find in backup chain page' %(chainName))
            return False
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/div/div[1]/button[2]').click()
        sleep(1)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        self.chainList.remove(chainName)
        return True
    
    def gotoBackupList(self, chainName):
        ''' goto  chain list page '''
        assert chainName != None and len(self.chainList) != 0
        assert chainName in self.chainList
        
        driver = self.driver
        driver.get(self.plate + self.backupChainPage)
        sleep(2)
        
        trs = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr')
        if trs[0].text == "没有找到匹配的记录": 
            print('chain list is empty')
            return False
        for tr in trs:
            volName = tr.find_element_by_xpath('.//td[3]/div').text
            if volName == chainName :
                tr.click()
                sleep(0.5)
                tr.find_element_by_xpath('.//td[3]').click()
                return True
        else:
            print('chain[%s] is not find in backup chain page' %(chainName))
            return False
    
    def addBackupPoint(self, chainName, pointName):
        ''' add backup point in backup list page '''
        assert chainName != None and pointName != None
        
        if self.gotoBackupList(chainName) == False:
            return False
        driver = self.driver
        driver.refresh()
        sleep(2)
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[1]').click()
        sleep(0.5)
        inp = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[2]/div/input')
        inp.clear()
        inp.send_keys(pointName)
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        return True
    
    def deletePoint(self, chainName, pointName):
        ''' add backup point in backup list page '''
        assert chainName != None and pointName != None
        
        if self.gotoBackupList(chainName) == False:
            return False
        driver = self.driver
        driver.refresh()
        sleep(2)
        
        backuBox = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[1]/div/div/div')
        
        inp = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/form/div[2]/div/input')
        inp.clear()
        inp.send_keys(pointName)
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[3]/div/div/button[1]').click()
        sleep(1)
        return True
    
    def recoverPoint(self, allVolume = True):
        pass
    
    def deletePointList(self):
        pass
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()