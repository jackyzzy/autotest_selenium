import unittest
import test_instance


def initInstanceSuit():    
    instanceSuit = unittest.TestSuite()
    instanceSuit.addTest(test_instance.TestInstance('test_00_create_linux'))
    instanceSuit.addTest(test_instance.TestInstance('test_01_create_win'))
    instanceSuit.addTest(test_instance.TestInstance('test_02_create_connect_del_instance'))
    instanceSuit.addTest(test_instance.TestInstance('test_03_start_poweroff_restart_outer'))
    instanceSuit.addTest(test_instance.TestInstance('test_04_start_powoff_restart_Force'))
    instanceSuit.addTest(test_instance.TestInstance('test_05_start_powoff_restart_inner'))
    instanceSuit.addTest(test_instance.TestInstance('test_11_mount_ultra_to_instance'))
    instanceSuit.addTest(test_instance.TestInstance('test_12_mount_high_to_instance'))
    instanceSuit.addTest(test_instance.TestInstance('test_13_create_backup'))
    instanceSuit.addTest(test_instance.TestInstance('test_14_create_all_backup'))
    instanceSuit.addTest(test_instance.TestInstance('test_15_umount_ultra_high_from_instance'))
    instanceSuit.addTest(test_instance.TestInstance('test_16_full_volume'))
    instanceSuit.addTest(test_instance.TestInstance('test_20_connect_outer'))
    instanceSuit.addTest(test_instance.TestInstance('test_21_write_read_file'))
    return instanceSuit


if __name__ == '__main__':
    suit = unittest.TestSuite()
    
    suit.addTest(initInstanceSuit())

    runer = unittest.TextTestRunner()
    runer.run(suit)
    