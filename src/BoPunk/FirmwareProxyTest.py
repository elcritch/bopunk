import unittest, hashlib
from FirmwareProxy import * 

class TestFirmwareProxy(unittest.TestCase):
    def setUp(self):
        self.firm = FakeFirm()

    def testFakeFirmware(self):
        assert_ = self.assert_
        assertEqual = self.assertEqual
        
        ret = self.firm.send('list')
        # print "list:\n", ret, 
        hash = hashlib.md5(ret).hexdigest()
        assertEqual( ret, "6ddef74e2a2d423f5b5f78c30e97cf85" )        
    
        ret = self.firm.send('info Rate')
        print "info:", ret
    
        ret = self.firm.send('get Rate')
        print "'get Rate':", ret
    
        ret = self.firm.send('set Rate 10')
        ret = self.firm.send('get Rate')
        print "'set/get Rate 10':", ret

    def testProxy(self):
        win = type('', (), {'variablesWidget':None})()
        proxy = FirmwareProxy(win)

    def testFirmVariable(self):
    
        ret = self.firm.send('list')
        print "list:\n", ret
    
        for line in ret.splitlines():
            print "\nline:", line
            var = FirmVariable(line)
            print "var.name", var.name
            print "var.default", var.default
            print "var.value", var.value
            print "var.min", var.min
            print "var.max", var.max
        
    



if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestCachedHandler)
    # suite.debug()
    # unittest.TextTestRunner(verbosity=4).run(suite)
