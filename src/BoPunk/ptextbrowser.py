#!/usr/bin/env python
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import QString, Qt, QVariant, SIGNAL, SLOT, QUrl, QByteArray
from PyQt4.QtGui import QImage, QPixmap
from PyQt4.QtGui import *

import sys, os, time
import urllib, urlparse

import BoPunk.lib.urlcache


class PTextBrowser(QTextBrowser):
    def __init__(self, cache=None, *args):
        """Init method."""
        QTextBrowser.__init__(self,*args)
        self.cache = cache

    def setResourceCache(self, cache):
        """Set the cache to use for this text browser."""
        self.cache = cache

    def loadResource(self, type, name):
        """Overloaded loadResource to provide http/url and caching support.

        Args:
        type -- type.
        name -- url beginning with http:// or file://.
        """
        url = unicode(name.toString())
        ret = QVariant()

        print "PTextBrowser:url:", url
        
        if not self.cache:
            sys.stderr.write("PTextBrowser: No URL Cache!\n")
            ret = QTextBrowser.loadResource(self, type, name)
        if url.startswith('http://') or url.startswith("file://"):
            try:
                res = self.cache.open(url)
                
                print "PTextBrowser:url:",res
                # reset file and read it in
                # http://groups.google.com/group/comp.lang.python/browse_thread/thread/8c83a50da6861887
                file = res.fp
                file.seek(0)
                ret = QVariant( QByteArray( file.read() ) )
            except Exception, inst:
                print "PTextBrowser:loadResource:exception:", inst
        else:
            print "PTextBrowser:res:", name

            ret = QTextBrowser.loadResource(self, type, name)
            
            if ret.isNull():
                # try adding url basename, to fix bug in QT 4.3
                base = unicode(self.source().toString())
                if base:
                    base = '/'.join(base.split("/")[:-1]) + "/" + url
                    print "PTextBrowser:other:", base
                    ret = self.loadResource(type, QUrl(base) )

        return ret

if __name__=="__main__":
    from sys import argv
    app=QApplication(argv)

    cacheloc = "../../cache/"
    cache = urlcache.build_opener(cacheloc)

    w = PTextBrowser(cache)
    w.show()

    html = "http://192.168.1.101/~jaremy/bopunk/firms/cool/firm1.html/index.html"
    # html = "file:///Users/jaremy/Sites/index.html"
    url = QUrl(html)
    print "url", url
    w.setSource(url)

    app.connect(app, SIGNAL("lastWindowClosed()")
                , app, SLOT("quit()"))
    app.exec_()
