#!/usr/bin/env python
from __future__ import absolute_import
 
import os, sys
import urllib, shutil
from urllib import quote, unquote
import threading, Queue
import urllib2
import time
from BoPunk.lib.ErrorClasses import *
from BoPunk.Settings import *

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
            try: 
                #grabs host from queue
                url, dst, done_sig = self.queue.get()
                self._url = url
                self._dst = dst
            
                # do work
                print "url, dst", url, dst
                self.retreive(url, dst)
            except Exception, inst:
                print "Fimware Cache Error:", inst
                self.signal(0, "Error Copying File")
                
            
            #signals to queue job is done
            self.queue.task_done()
            time.sleep(3)
            self.done(done_sig,(url,dst))

    def retreive(self, url, dst):
        print "FirmCache getfirm '%s' to '%s'" % (url, dst)
        # TODO: check date and update file
        
        # get firmware from either cache file or from http url
        if url.startswith("file://") and os.path.isfile(url[7:]):
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
            print "OSError:", inst
        
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
    def __init__(self, signal, done):
        """creates a simple cacheing for firmwares"""
        cache = Settings()['firmware_cache']
        cache = os.path.abspath(cache)
        
        print "DEBUG: curdir:",os.path.abspath(os.curdir)
        print "DEBUG: cache:",cache
        if not os.path.isdir(cache):
            try:
                print "Making firmware cache"
                os.makedirs(cache)
            except (OSError), inst:
                line = "FirmCache: Couldn't Create cache: ERROR:"
                print "OSError:",line, str(inst), inst.strerror
                raise AppError(line, exit=True)
                
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
    
    print "os.path.abspath()", os.path.abspath(".")
    SETTINGS = {
        "firmware_cache":"../cache/firms/",
        "image_cache":"../cache/imgs/"
    }
    
    def testsignal(*val):
        print "testsignal: val", val
    
    def donesignal():
        print "donesignal"
    
    print "Starting cache..."
    loc = "http://www.bocolab.org/bopunks/example2/example2.bin"    
    firmloc = "/tmp/firmcache/"
    cache = FirmCache(testsignal, donesignal)
    cache.clear()
    
    try: 
        cache.getfirm(loc)
    except Exception, inst:
        print "Exception:", inst
        import traceback
        traceback.print_stack()
        traceback.print_exc()
        
    
    
    cache.queue.join()
    sys.exit(0)