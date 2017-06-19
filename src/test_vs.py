# coding=utf-8
from time import sleep
import unittest
import instance
import volume
import config

class TestInstance(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.instance = instance.Instance(config.plate)
        self.instance.login()

    @classmethod
    def tearDownClass(self):
        self.instance.logout()
        
    def test_01_create_del_instance(self):
        vm = self.instance.create_instance()
        sleep(30)
#         vm = "test"
#         self.vmlist.append(vm)
        self.instance.connect(vm)
        self.instance.delete_instance(vm)
    
    def test_02_start_powoff_restart_inner(self):
        vm = self.instance.create_instance()
        sleep(30)
                
        '''after shutdown inner, check status in page'''
        self.instance.shutdown_instance_inner(vm)
        sleep(600)
        if self.instance.get_instance_status(vm) != '已关闭':
            print("shutdown in instance, but still not in page")
            return False
        
        self.instance.start_instance(vm)
        sleep(100)
        if self.instance.get_instance_status(vm) != '运行中':
            print('start no success.')
            return False
        
        self.instance.restart_instance_inner(vm)
        sleep(100)
        if self.instance.get_instance_status(vm) != '运行中':
            print ('restart no success')
            return False
        
        return True
    
    def test_03_start_poweroff_restart_outer(self):
        vm = self.instance.create_instance()
        sleep(30)
                
        '''after shutdown inner, check status in page'''
        self.instance.shutdown_instance_outer(vm)
        sleep(30)
        if self.instance.get_instance_status(vm) != '已关闭':
            print("shutdown in instance, but still not in page")
            return False
        
        self.instance.start_instance(vm)
        sleep(60)
        if self.instance.get_instance_status(vm) != '运行中':
            print('start no success.')
            return False
        
        self.instance.restart_instance_outer(vm)
        sleep(100)
        if self.instance.get_instance_status(vm) != '运行中':
            print ('restart no success')
            return False
        
        return True

if __name__ == '__main__':
    unittest.main()