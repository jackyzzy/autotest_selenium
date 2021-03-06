# coding=utf-8
from selenium import webdriver
from time import sleep
import unittest
from random import randint
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import check
from _ast import Try
from test.test_tools.test_unparse import try_except_finally
from selenium.common import exceptions as SEE


plate="http://100.86.0.1"
instance="/dashboard/host/#host"

class TestInstance(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.vmlist = []
        self.vmcnt = randint(2,100)
        self.vmbase = "test"
        self.vmpw = "admin123"
        self.check = check.Check();
        self.driver = webdriver.Chrome()
#         self.driver = webdriver.Edge()
        
        driver = self.driver
        driver.get(plate)
        driver.delete_all_cookies()
        driver.refresh()
        
        ''' login '''
        driver.find_element_by_id("id_username").send_keys("zzy@sangfor.com")
#         driver.find_element_by_id("id_username").send_keys("acloud@sangfor.com")
        driver.find_element_by_id("id_password").send_keys("Admin12345")
        driver.find_element_by_id("loginBtn").click()
        sleep(0.5)

    @classmethod
    def tearDownClass(self):
#         super(TestCreateInstance, cls).tearDownClass()
        driver = self.driver
        ''' clear env '''
#         sleep(3)
        driver.quit()
        
    def create_instance(self):
        '''
        create instance
        '''
        
        driver = self.driver
        # go to plate page
        driver.get(plate+instance)
        sleep(2)
        
        # click new instance
#         driver.find_element_by_id("plate-btn-create-computer").click()  
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/button[1]').click()
        sleep(1)
        
        # select image
        driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div[3]/ul/li[1]/div").click()
#         driver.find_element_by_xpath("//*[@class='plate-add-image-detail-panel plate-add-image-common-panel']/ul/li[1]/div").click()
        
        # click next after image
        driver.find_element_by_xpath("//*[@class='btn btn-primary btn-submit']").click()
#         driver.find_element_by_xpath("//*[@id='site-my-list']/ul/li[2]/div").click()
        
        # click next after configuration
        driver.find_element_by_xpath('html/body/div[5]/div/div[2]/div/div[3]/div/div/button[2]').click()
        # click next after networking
        driver.find_element_by_xpath('html/body/div[5]/div/div[2]/div/div[3]/div/div/button[2]').click()
        
        # click go after base inrormation: instance name, pw
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
        sleep(5)
        self.vmlist.append(vmname)
        self.vmcnt = self.vmcnt + 1
        print(self.vmlist)
        return vmname
    
    def delete_instance(self, vmname):
        ''' 
        delete instance 
        '''
        assert len(self.vmlist) != 0
        assert vmname in self.vmlist
        
        driver = self.driver
        # go to plate page
        driver.get(plate+instance)
        sleep(2)

        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return
            
            checkInp = td.find_element_by_xpath(".//td[1]/input")
            checkLable = td.find_element_by_xpath(".//td[1]/label")
#             status = td.find_element_by_xpath('.//td[2]/span[@title="运行中"]')
            status = td.find_element_by_xpath('.//td[2]/span')
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
        driver.get(plate+instance)
        sleep(2)
        rd = driver.find_elements_by_xpath('//*[@id="content-body"]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr')
        for td in rd:
            ''' no instance continue'''
            if td.text == "没有找到匹配的记录":
                return False
            
            checkInp = td.find_element_by_xpath(".//td[1]/input")
            checkLable = td.find_element_by_xpath(".//td[1]/label")
#             status = td.find_element_by_xpath('.//td[2]/span[@title="运行中"]')
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

#             td.click()
            print(checkInp.id)
            print(status.get_attribute('title'))
            print(instanceName.text)
            print(img)
            print(iip)
            print(pip)
#             instanceName.find_element_by_xpath('.//*[@class="host-list-detail-link"]').click()
#             sleep(3)
#             driver.back()
            ''' only lable can be multi select ''' 
#             checkLable.click()
            if self.check.check_ip(pip, 22, 'root', self.vmpw, iip):
                print("public ip connected !")
                return True
            else :
                print("public ip not connected !")
                return False
        
    def shutdown_instance(self):
        pass
    
    def test_01_create_del_instance(self):
        vm = self.create_instance()
        sleep(30)
#         vm = "test"
#         self.vmlist.append(vm)
        self.connect(vm)
        self.delete_instance(vm)
    
    def test_02_start_powoff_restart_inner(self):
        vm = self.create_instance()
        sleep(30)
    
    def test_03_start_poweroff_restart_outer(self):
        pass

if __name__ == '__main__':
    unittest.main()