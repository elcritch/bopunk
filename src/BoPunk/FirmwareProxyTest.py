import unittest, hashlib
from FirmwareProxy import * 
from bopunk_sim import *

class TestFirmwareProxy(unittest.TestCase):
    def setUp(self):
        self.firm = FakeFirm()
    
    def testProxy(self):
        win = type('', (), {'variablesWidget':None})()
        proxy = FirmwareProxy(win)
    
        
    



if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestCachedHandler)
    # suite.debug()
    # unittest.TextTestRunner(verbosity=4).run(suite)
