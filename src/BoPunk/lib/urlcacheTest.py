import unittest
from urlcache import *

class TestCachedHandler(unittest.TestCase):
    """provides initial url cache testing.

    TODO: udate for new cache code.
    """
    def setUp(self):
        import tempfile
        loc = tempfile.mkdtemp(suffix='urlcache')
        self.cache = build_opener(loc)

        self.assert_( 'open' in dir(self.cache), 'no cache')

    def testUrl(self):
        url = "http://onyx.boisestate.edu/~jcreechl/bopunk/feeds/firms.atom.xml"
        # print("url", url)

        f1 = self.cache.open(url)
        read = f1.read()
        # print("f1:", hashlib.md5(f1.read()).hexdigest())

    def testImg(self):
        img = self.cache.open("http://onyx.boisestate.edu/~jcreechl/bopunk/firms/cool/firm1.html/images/macosxlogo.png")
        hash1 = hashlib.md5(img.read()).hexdigest()
        # print("hash img:", hash1)

        img2 = self.cache.open("http://onyx.boisestate.edu/~jcreechl/bopunk/firms/cool/firm1.html/images/macosxlogo.png")
        hash2 = hashlib.md5(img2.read()).hexdigest()
        self.assertEqual( hash1, hash2 )

        # img.dononething()


    def testFile(self):
        tf1 = self.cache.open("file://%s/urlcache.py"%os.path.abspath('.'))
        self.assert_( 'seek' in dir(tf1) )
        self.assert_( 'read' in dir(tf1) )

        tf2 = self.cache.open("file://%s/urlcache.py"%os.path.abspath('.'))
        self.assert_( 'seek' in dir(tf1) )
        self.assert_( 'read' in dir(tf1) )

        hash1 = hashlib.md5(tf1.read()).hexdigest()
        hash2 = hashlib.md5(tf2.read()).hexdigest()
        self.assertEqual( hash1, hash2 )

if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestCachedHandler)
    # suite.debug()
    # unittest.TextTestRunner(verbosity=4).run(suite)
