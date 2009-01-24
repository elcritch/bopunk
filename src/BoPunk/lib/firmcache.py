#!/usr/bin/python2.5
 
import os, sys
import urllib, shutil
from urllib import quote, unquote

import threading, Queue
import urllib2
import time


class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue, cache, signal, done):
        threading.Thread.__init__(self)
        self.queue = queue
        self.cache = cache
        self.signal = signal
        self.done = done
        
    def run(self):
        while True:
            #grabs host from queue
            url, dst, done_sig = self.queue.get()
            self._url = url
            self._dst = dst
            
            # do work
            print "url, dst", url, dst
            self.retreive(url, dst)
            self.done(done_sig,(url,dst))
            
            #signals to queue job is done
            self.queue.task_done()

    def retreive(self, url, dst):
        print "FirmCache getfirm '%s' to '%s'" % (url, dst)
        # TODO: check date and update file
        
        # get firmware from either cache file or from http url
        if url.startswith("file://"):
            print "FirmCache: getting file"
            shutil.copy( url[7:], dst )
            self.signal(100, "Completing Copying File")
        else:
            print "FirmCache: getting url"
            self.geturl(url,dst)

    def geturl(self, url, dst):
        """retreives firmware bin, must use ATOM id for dst source."""
        dirs = os.path.split(dst)[0]
        print "dirs:", dirs
        try:
            os.makedirs(dirs)
        except OSError, inst:
            print "inst", inst
        
        urllib.urlretrieve(url, dst, self._reporthook)
    
    def _reporthook(self, numbcacheks, bcacheksize, filesize):
        # print "reporthook(%s, %s, %s)" % (numbcacheks, bcacheksize, filesize)
        base = os.path.basename(self._url)
        # Should handle possible filesize=-1.
        try:
            percent = min((numbcacheks*bcacheksize*100)/filesize, 100)
        except:
            percent = 100

        if numbcacheks != 0:
            # sys.stdout.write("\b"*70)
            pass
        self.signal(percent, "Downloading %s"%self._url)
    



class FirmCache:
    def __init__(self, signal, done, cache="firmcache/"):
        """creates a simple cacheing for firmwares"""
        cache = os.path.abspath(cache)
        
        if not os.path.isdir(cache):
            try:
                print "Making firmware cache"
                os.mkdir(cache)
            except os.OSError, inst:
                print "FirmCache: Couldn't Create cache: ERROR:", inst
                raise AppError(exit=True)
                
        self.cache = cache
        self._signal = signal
        self.queue = Queue.Queue()
        
        self.getter = ThreadUrl(self.queue, self.cache, signal, done)
        self.getter.start()
        
    def getfirm(self, item, done_sig):
        """
        uses an ATOM entry to retreive firmware cache
        """
        self._item = item
        
        # src
        url = item['links'][0]['href']
            
        # 'tag:boPunk,2009-01-12:/manual/id0'
        idpath = item['id'].split(':')[-1]
        id = os.path.join(*idpath.split('/'))
        dst = os.path.join( self.cache, id+'.bin' ) 
        
        self.queue.put((url,dst, done_sig))
    
        
    def clear(self):
        shutil.rmtree(self.cache)
        os.mkdir(self.cache)
        



if __name__ == "__main__":
    from .. import FirmwareFeed 
    
    def testsignal(*val):
        print "testsignal: val", val

    def donesignal():
        print "donesignal"
    
    loc = "http://192.168.1.101/~jaremy/bopunk/feeds/firms.atom.xml"
    atom = FirmwareFeed.FirmwareFeed(loc)
    item = atom[0]
    # print "item", item
    print "Starting cache..."
    
    cache = FirmCache(testsignal, donesignal)
    cache.clear()
    
    try: 
        cache.getfirm(item)
    except Exception, inst:
        print "inst", inst
    
    
    cache.queue.join()
    sys.exit(0)