# coding=utf-8
from time import sleep
import envConfig
import unittest
import instance
import volume


class TestInstance(unittest.TestCase):
    
    def getFileName(self):
        import sys
        try:
            raise Exception
        except:
            exc_info = sys.exc_info()
            traceObj = exc_info[2]
            frameObj = traceObj.tb_frame
            ''' func & line in current function '''
            Upframe = frameObj.f_back
            ''' func & line in upstream(call) function '''
            return Upframe.f_code.co_filename
        
    def getFuncName(self):
        import sys
        try:
            raise Exception
        except:
            exc_info = sys.exc_info()
            traceObj = exc_info[2]
            frameObj = traceObj.tb_frame
            ''' func & line in current function '''
            Upframe = frameObj.f_back
            ''' func & line in upstream(call) function '''
            return Upframe.f_code.co_name
        
    def getLineNum(self):
        import sys
        try:
            raise Exception
        except:
            exc_info = sys.exc_info()
            traceObj = exc_info[2]
            frameObj = traceObj.tb_frame
            ''' func & line in current function '''
            Upframe = frameObj.f_back
            ''' func & line in upstream(call) function '''
            return Upframe.f_lineno
    
    @classmethod
    def setUpClass(self):
        self.instance = instance.Instance(envConfig.plate)
        self.instance.login()
        self.volume = volume.Volume(envConfig.plate)
        self.volume.login()

    @classmethod
    def tearDownClass(self):
        self.instance.logout()
        self.volume.logout()

    def setUp(self):
        unittest.TestCase.setUp(self)
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
    
    def test_00_create_linux(self):
        if 'linux' not in self.instance.vmlist:
            self.assertEqual(self.instance.createInstance('linux', 'cen'), 'linux', '[test_00_create_linux] instance[linux] create fail')
            sleep(60)
            #TODO: check ping
            
    def test_01_create_win(self):
        if 'win' not in self.instance.vmlist:
            self.assertEqual(self.instance.createInstance('win', 'win'), 'win', '[test_01_create_win] instance[win] create fail')
            sleep(60)
            #TODO: check ping
    
    def test_02_create_connect_del_instance(self):
        curFunc = self.getFuncName()
        vm = self.instance.createInstance(image = 'cen')
        self.assertIsNotNone(vm, 'create vm[%s] fail in %s' %(vm, curFunc))
        sleep(60)
        self.assertTrue(self.instance.connect(vm), 'vm[%s] can not be connected in %s' %(vm, curFunc))
        sleep(3)
        self.assertTrue(self.instance.deleteInstance(vm), 'delete vm[%s] false in %s' %(vm, curFunc))
        #TODO: check ping
        
    def test_03_start_poweroff_restart_outer(self):
        curFunc = self.getFuncName()
        vm = self.instance.createInstance()
        self.assertIsNotNone(vm, 'create vm fail in %S' %(curFunc))
        sleep(30)
        
        #TODO: check ping
        '''after shutdown inner, check status in page'''
        self.assertTrue(self.instance.shutdownOuter(vm), 'fail to shutdown instance[%s] outer in %s' %(vm, curFunc))
        sleep(60)
        self.assertEqual(self.instance.getInstanceStatus(vm), '已关机', "instance[%s] is not closed, after shutdownOuter in %s" %(vm, curFunc))
        
        self.assertTrue(self.instance.startInstance(vm), 'fail to start instance[%s] in %s' %(vm, curFunc))
        sleep(100)
        self.assertEqual(self.instance.getInstanceStatus(vm), '运行中', 'instance[%s] status is not running after startInstance outer in %s' %(vm, curFunc))
        
        self.assertTrue(self.instance.restartOuter(vm), 'fail to restart instance[%s] in %s' %(vm, curFunc))
        sleep(120)
        self.assertEqual(self.instance.getInstanceStatus(vm), '运行中', 'instance[%s] status is not running after restartOuter in %s' %(vm, curFunc))
    
    def test_04_start_powoff_restart_Force(self):
        curFunc = self.getFuncName()
        vm = self.instance.createInstance()
        self.assertIsNotNone(vm, 'create vm fail in %s' %(curFunc))
        sleep(30)
        
        #TODO: check ping
        '''after shutdown inner, check status in page'''
        self.assertTrue(self.instance.shutdownOuterForce(vm), 'fail to shutdown instance[%s] outer in %s' %(vm, curFunc))
        sleep(120)
        self.assertEqual(self.instance.getInstanceStatus(vm), '已关机', "instance[%s] is not closed, after shutdownOuter in %s" %(vm, curFunc))
        
        self.assertTrue(self.instance.startInstance(vm), 'fail to start instance[%s] in %s' %(vm, curFunc))
        sleep(60)
        self.assertEqual(self.instance.getInstanceStatus(vm), '运行中', 'instance[%s] status is not running after startInstance outer in %s' %(vm, curFunc))
        
        self.assertTrue(self.instance.restartOuter(vm), 'fail to restart instance[%s] in %s' %(vm, curFunc))
        sleep(160)
        self.assertEqual(self.instance.getInstanceStatus(vm), '运行中', 'instance[%s] status is not running after restartOuter in %s' %(vm, curFunc))
    
    def test_05_start_powoff_restart_inner(self):
        curFunc = self.getFuncName()
        vm = self.instance.createInstance(image = 'cen')
        self.assertIsNotNone(vm, 'create vm fail in %s' %(curFunc))
        sleep(60)
                
        #TODO: check ping
        '''after shutdown inner, check status in page'''
        self.assertTrue(self.instance.shutdownInner(vm), 'fail to close vm[%s] in %s' %(vm, curFunc))
        sleep(600)
        self.assertEqual(self.instance.getInstanceStatus(vm), '已关机', "instance[%s] is not closed, after shutdownInner in %s" %(vm, curFunc))
        
        self.assertTrue(self.instance.startInstance(vm), 'fail to start instance[%s] in %s' %(vm, curFunc))
        sleep(100)
        self.assertEqual(self.instance.getInstanceStatus(vm), '运行中', 'instance[%s] is not running, after startInstance in %s' %(vm, curFunc))
        
        self.assertTrue(self.instance.restartInner(vm), 'fail to restart[%s] Inner in %s' %(vm, curFunc))
        sleep(600)
        self.assertEqual(self.instance.getInstanceStatus(vm), '运行中', 'instance[%s] status is not running after restartOuter in %s' %(vm, curFunc))
    
    def test_11_mount_ultra_to_instance(self):
        curFunc = self.getFuncName()
        vmname = 'linux'
        ultrax_volume = 'test11_ultrax'
        if vmname not in self.instance.vmlist:
            self.assertEqual(self.instance.createInstance(vmname, 'cen'), vmname, 'fail to create vm in %s' %(curFunc))
            sleep(30)
        if self.instance.getInstanceStatus(vmname) != '已关机':
            self.assertTrue(self.instance.shutdownOuter(vmname), 'fail to shutdown vm[%s] in %s' %(vmname, curFunc))
            sleep(100)
        self.assertTrue(self.volume.createVolume(ultrax_volume, 'ultrax'), 'fail to create volume[%s] in %s' %(ultrax_volume, curFunc))
        sleep(20)
        self.assertTrue(self.instance.mountVolume(vmname, ultrax_volume), 'fail to mount volume[%s] to instance[%s] in %s' %(ultrax_volume, vmname, curFunc))
        sleep(20)
        
        self.assertTrue(self.instance.startInstance(vmname), 'fail to start vm[%s] in %s' %(vmname, curFunc))
        sleep(60)
        #TODO: check ping
        
    def test_12_mount_high_to_instance(self):
        curFunc = self.getFuncName()
        vmname = 'linux'
        high_volume = 'test12_high'
        if vmname not in self.instance.vmlist:
            self.assertEqual(self.instance.createInstance(vmname, 'cen'), vmname, 'fail to create vm in %s' %(curFunc))
            sleep(30)
        if self.instance.getInstanceStatus(vmname) != '已关机':
            self.assertTrue(self.instance.shutdownOuter(vmname), 'fail to shutdown instance[%s] in %s' %(vmname, curFunc))
            sleep(100)
        self.assertTrue(self.volume.createVolume(high_volume, 'high'), 'fail to create volume[%s] in %s' %(high_volume, curFunc))
        sleep(20)
        self.assertTrue(self.instance.mountVolume(vmname, high_volume), 'fail to mount volume[%s] to instance[%s] in %s' %(high_volume, vmname, curFunc))
        sleep(20)
        
        self.assertTrue(self.instance.startInstance(vmname), 'fail to start instance in %s' %(vmname, curFunc))
        sleep(60)
        #TODO: check ping   
        
    def test_12_create_backup(self):
        curFunc = self.getFuncName()
        vmname = 'linux'
        if vmname not in self.instance.vmlist:
            self.assertTrue(self.instance.createInstance(vmname, 'linux'), 'fail to create vm in %s' %(curFunc))
            sleep(30)
        
        self.assertTrue(self.instance.createBackup(vmname, 'mannal1'), 'fail to create instance[%s]system volume backup in %s' %(vmname, curFunc))
        sleep(60)
        
    def test_13_create_all_backup(self):
        curFunc = self.getFuncName()
        vmname = 'linux'
        if vmname not in self.instance.vmlist:
            self.assertTrue(self.instance.createInstance(vmname, 'linux'), 'fail to create vm in %s' %(curFunc))
            sleep(30)
        
        self.assertTrue(self.instance.createBackup(vmname, 'mannal2', True), 'fail to create instance[%s] system volume backup in %s' %(vmname, curFunc))
        sleep(60)
    
    def test_14_umount_ultra_high_from_instance(self):
        curFunc = self.getFuncName()
        vmname = 'linux'
        ultrax_volume = 'test11_ultrax'
        high_volume = 'test12_high'
                
        self.assertIn(vmname, self.instance.vmlist, 'instance[%s] not exit in %s' %(vmname, curFunc))
        
        if self.instance.getInstanceStatus(vmname) != '已关机':
            self.assertTrue(self.instance.shutdownOuter(vmname), 'fail to shutdown instance[%s] in %s' %(vmname, curFunc))
            sleep(120)
        
        self.assertIn(ultrax_volume, self.volume.volList, 'volume[%s] not exist in  %s' %(ultrax_volume, curFunc))
        self.assertTrue(self.instance.umountVolume(vmname, ultrax_volume), 'fail to umount volume[%s] from instance[%s] in %s' %(ultrax_volume, vmname, curFunc))
        sleep(20)
        
        self.assertIn(high_volume, self.volume.volList, 'volume[%s] not exist in %s' %(high_volume, curFunc))
        self.assertTrue(self.instance.umountVolume(vmname, high_volume), 'fail to umount volume[%s] from instance[%s] in %s' %(high_volume, vmname, curFunc))
        sleep(20)
        
        self.assertTrue(self.instance.startInstance(vmname), 'fail to start instance[%s] in %s' %(vmname, curFunc))
        sleep(60)
        #TODO: check ping
    
    def test_15_full_volume(self):
        curFunc = self.getFuncName()
        vm = self.instance.createInstance(image = 'cen')
        self.assertIsNotNone(vm, 'fail to create vm in %s' %(curFunc))
        self.assertTrue(self.instance.shutdownOuter(vm), 'fail to shutdown instance[%s] in %s' %(vm, curFunc))
        sleep(600)
        vol1 = '%s_1' % (vm)
        vol2 = '%s_2' % (vm)
        vol3 = '%s_3' % (vm)
        vol4 = '%s_4' % (vm)
        self.assertTrue(self.volume.createVolume(vol1, 'ultra'), 'fail to create volume in %s' %(curFunc))
        sleep(2)
        self.assertTrue(self.volume.createVolume(vol2, 'ultra'), 'fail to create volume in %s' %(curFunc))
        sleep(2)
        self.assertTrue(self.volume.createVolume(vol3, 'ultra'), 'fail to create volume in %s' %(curFunc))
        sleep(2)
        self.assertTrue(self.volume.createVolume(vol4, 'ultra'), 'fail to create volume in %s' %(curFunc))
        sleep(2)
        
        self.assertTrue(self.instance.mountVolume(vm, vol1), 'fail to mount volume[%s] to instance[%s] in %s' %(vol1, vm, curFunc))
        sleep(5)
        self.assertTrue(self.instance.mountVolume(vm, vol2), 'fail to mount volume[%s] to instance[%s] in %s' %(vol2, vm, curFunc))
        sleep(5)
        self.assertTrue(self.instance.mountVolume(vm, vol3), 'fail to mount volume[%s] to instance[%s] in %s' %(vol3, vm, curFunc))
        sleep(5)
        self.assertTrue(self.instance.mountVolume(vm, vol4), 'fail to mount volume[%s] to instance[%s] in %s' %(vol4, vm, curFunc))
        sleep(15)
        
        self.assertTrue(self.instance.startInstance(vm), 'fail to start instance[%s] in %s' %(vm, curFunc))
        sleep(30)
        self.assertTrue(self.instance.connect(vm), 'fail to connet instance[%s] in %s' %(vm, curFunc))
        self.assertTrue(self.instance.shutdownOuter(vm), 'fail to shutdown instance[%s] in %s' %(vm, curFunc))
        sleep(100)
        
        self.assertTrue(self.instance.umountVolume(vm, vol1), 'fail to mount volume[%s] from instance[%s] in %s' %(vol1, vm, curFunc))
        sleep(5)
        self.assertTrue(self.instance.umountVolume(vm, vol2), 'fail to mount volume[%s] from instance[%s] in %s' %(vol2, vm, curFunc))
        sleep(5)
        self.assertTrue(self.instance.umountVolume(vm, vol3), 'fail to mount volume[%s] from instance[%s] in %s' %(vol3, vm, curFunc))
        sleep(5)
        self.assertTrue(self.instance.umountVolume(vm, vol4), 'fail to mount volume[%s] from instance[%s] in %s' %(vol4, vm, curFunc))
        sleep(5)
        
    def test_20_connect_outer(self):
        curFunc = self.getFuncName()
        vm = 'linux'
        if vm not in self.instance.vmlist:
            self.assertTrue(self.instance.createInstance(vm, 'cen'), 'fail to create instance in %s' %(curFunc))
            sleep(60)
        if self.instance.getInstanceStatus(vm) != '运行中':
            self.assertTrue(self.instance.startInstance(vm), 'fail to start instance[%s] in %s' %(vm, curFunc))
            sleep(100)
        
        self.assertTrue(self.instance.vmPingHost(vm), 'cannot ping from instance[%s] to host[%s] in %s' %(vm, envConfig.ip, curFunc))
    
    def test_21_write_read_file(self):
        curFunc = self.getFuncName()
        vm = 'linux'
        if vm not in self.instance.vmlist:
            self.assertTrue(self.instance.createInstance(vm, 'cen'), 'fail to create instance[%s] in %s' %(vm, curFunc))
            sleep(60)
        if self.instance.getInstanceStatus(vm) != '运行中':
            self.assertTrue(self.instance.startInstance(vm), 'fail to start vm[%s] in %s' %(vm, curFunc))
            sleep(100)
        
        file = 'aaa.txt'
        contain = 'bbbbbbbb'
        
        self.assertTrue(self.instance.vmWriteLine(vm, contain, file), 'fail to write line[\'%s\'] onto instance[%s] in %s' %(contain, vm, curFunc))
        self.assertEqual(self.instance.vmReadLine(vm, file), contain, 'read is not equal with write on instance[%s] in %s' %(vm, curFunc))
    
    