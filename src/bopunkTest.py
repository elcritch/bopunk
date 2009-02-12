import unittest, hashlib
from bopunk import *


class TestFirmwareProxy(unittest.TestCase):
    def setUp(self):
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
    
    def testProxy(self):
        print "proxy", self.proxy
        
        exit(1)
        
    
    



if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestCachedHandler)
    # suite.debug()
    # unittest.TextTestRunner(verbosity=4).run(suite)
