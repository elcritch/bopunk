#!/usr/bin/env python
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import QString, Qt, QVariant, SIGNAL, SLOT, QUrl, QByteArray
from PyQt4.QtGui import *

import sys, os, time 
import urllib, urlparse

import BoPunk.lib.urlcache


class PTextBrowser(QTextBrowser):
    def __init__(self, cache=None, *args):
        QTextBrowser.__init__(self,*args)
        self.cache = cache
        print "DEBUG: PTextBrowser Running!"
    
    def setResourceCache(self, cache):
        """set the cache to use for this text browser"""
        self.cache = cache
    
    def loadResource(self, type, name):
        """overloaded loadResource to provide http/url and caching support"""
        url = unicode(name.toString())
        ret = QVariant()
        
        if not self.cache:
            sys.stderr.write("PTextBrowser: No URL Cache!\n")
            ret = QTextBrowser.loadResource(self, type, name)
            return ret
        
        if url.startswith('http://') or url.startswith("file://"):
            try:
                res = self.cache.open(url)
                # reset file and read it in
                file = res.fp
                file.seek(0)
                ret = QVariant( QByteArray( file.read() ) )                
            except Exception, inst:
                print "loadResource: exception:", inst
                return ret
        else:
            print "loadResource: loading DEFAULT RESOURCE:", url
            
            ret = QTextBrowser.loadResource(self, type, name)
            
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
