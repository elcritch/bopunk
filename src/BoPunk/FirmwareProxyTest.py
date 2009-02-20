import unittest, hashlib
from FirmwareProxy import *
from bopunk_sim import *

class TestFirmwareProxy(unittest.TestCase):
    """Initial support for autmated testing of firmware proxy."""
    def setUp(self):
        """Setup initial firmware proxy or simulator."""
        win = type('', (), {'variablesWidget':None})()
        self.proxy = FirmwareProxy(win)


    def testProxy(self):
        """TODO: test proxy."""
        print "proxy", self.proxy





if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestCachedHandler)
    # suite.debug()
    # unittest.TextTestRunner(verbosity=4).run(suite)
