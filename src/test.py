import unittest
import test_instance

class Test_my(unittest.TestCase):
    def add(self, a = 10, b = 10):
        return a + b;
    def test_01(self):
        self.assertEqual(20, self.add(10, 10),'result not equal')
        
    def test_02(self):
        self.assertIsNotNone('a', 'none')

if __name__ == '__main__':
    suit = unittest.TestSuite()
    suit.addTest(Test_my('test_01'))
    suit.addTest(Test_my('test_02'))
#     suit.addTest(test_instance.TestInstance('test_20_connect_outer'))
    suit.addTest(test_instance.TestInstance('test_05_start_powoff_restart_inner'))
    runer = unittest.TextTestRunner()
    runer.run(suit)