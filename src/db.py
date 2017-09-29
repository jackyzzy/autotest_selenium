# coding=utf-8
from selenium import webdriver
from time import sleep
import envConfig

class RDS():
    ''' rds db test case
    >>> pp = "http://100.1.22.1"
        
    >>> policy = 'aaa'
    
    >>> bkp = RDS(pp)
    
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
        self.RDSPage = envConfig.RDSPage
        self.userName = envConfig.userName
        self.passwd = envConfig.passWD
        self.driver = webdriver.Chrome()
        self.RDSList = self.getRDSList()
        
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
    
    def createRDS(self):
        pass
    
    def deleteRDS(self):
        pass
        
    def renameRDS(self):
        pass
    
    def changePW(self):
        pass
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()