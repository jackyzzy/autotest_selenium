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
    runer = unittest.TextTestRunner()
    runer.run(suit)