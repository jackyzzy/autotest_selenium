# coding=utf-8
from time import sleep
import unittest
import envConfig
import rds


class TestRDS(unittest.TestCase):
    
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
        self.rds = rds.RDS(envConfig.plate)
        self.rds.login()

    @classmethod
    def tearDownClass(self):
        self.rds.clearRDS()
        self.rds.logout()

    def setUp(self):
        unittest.TestCase.setUp(self)
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
    
    def test_00_create_rds(self):
        self.assertEqual(self.rds.createRDS('test_000', 'admin123'), 'test_000', '[test_00_create_rds]: rds[test_000] create fail')
        sleep(200)
            
    def test_01_create_rename_delete(self):
        self.assertEqual(self.rds.createRDS('test_001', 'admin123'), 'test_001', '[test_01_create_rename_delete]: rds[test_001] create fail')
        sleep(200)
        self.assertIsNone(self.rds.renameRDS('test_001', 'rename_001'), '[test_01_create_rename_delete]: rename rds[test_001] to rds[rename_001] fail')
        sleep(10)
    
    def test_02_create_changpw_delete(self):
        self.assertEqual(self.rds.createRDS('test_002', 'admin123'), 'test_002', '[test_02_create_changpw_delete]: rds[test_002] create fail')
        sleep(200)
        self.assertIsNone(self.rds.changePW('test_002', 'test12345'), '[test_02_create_changpw_delete]: chang pw to rds[test_002] fail')
        sleep(10)
        self.assertIsNone(self.rds.deleteRDS('test_002'), '[test_02_create_changpw_delete]: rds[test_002] delete fail')
        sleep(10)
        
    def test_03_create_delete(self):
        self.assertEqual(self.rds.createRDS('test_003', 'admin123'), 'test_003', '[test_03_create_delete]: rds[test_003] create fail')
        sleep(200)
        self.assertIsNone(self.rds.deleteRDS('test_003'), '[test_03_create_delete]: rds[test_003] delete fail')
        sleep(10)
    
    def test_04_create_clear(self):
        self.assertEqual(self.rds.createRDS('test_004', 'admin123'), 'test_004', '[test_04_create_clear]: rds[test_004] create fail')
        sleep(200)
        self.assertIsNone(self.rds.clearRDS(), '[test_04_create_clear]: clear fail')
