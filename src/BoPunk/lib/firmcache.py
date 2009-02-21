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
    """Threaded Url Grab.

    Uses a consumer/producer model based on pyhton queue to communicate. To use,
    place tuple containing correct data onto the queue. A signal given with the url
    will be emitted with percent download and a message also given with url.
    Once the url is downloaded a signal as given at initialization time will be emitted
    to reset any messages. The default reset delay is 3 seconds.
    """
    def __init__(self, queue, cache, signal, done):
        """initializes url downloader.

        Args:
        queue -- work queue.
        cache -- cache to used for downloading/caching.
        signal -- finalize signal emitted after download complete, returns resource.
        done -- function to be called to emit signal.
        """
        threading.Thread.__init__(self)
        self.queue = queue
        self.cache = cache
        self.signal = signal
        self.done = done
        self.settings = Settings()

    def run(self):
        """implements worker loop. """
        while True:
            try:
                #grabs host from queue
                pdate, url, dst, done_sig = self.queue.get()
                self._pdate = pdate
                self._url = url
                self._dst = dst

                # do work
                print "pdate, url, dst", pdate, url, dst
                self.retreive(pdate, url, dst)
            except Exception, inst:
                print "Fimware Cache Error:", inst
                self.signal(0, "Error Copying File")


            #signals to queue job is done
            self.queue.task_done()
            time.sleep(3)
            self.done(done_sig,(url,dst))

    def retreive(self, pdate, url, dst):
        """retreives urls, either url:// or file:// urls. """
        print "FirmCache getfirm '%s' to '%s'" % (url, dst)
        # TODO: check date and update file
        dst_dt = None
        if os.path.isfile(dst):
            dst_dt = time.gmtime(os.path.getmtime(dst))
        
        if dst_dt >= pdate:
            # then local cache is current
            self.signal(100, "Firmware already update to date.")
        elif url.startswith("file://") and os.path.isfile(url[7:]):
            # get firmware from either cache file or from http url
            print "FirmCache: getting file"
            shutil.copy( url[7:], dst )
            self.signal(100, "Completing Copying File")
        else:
            # default retrieve url 
            print "FirmCache: getting url"
            self.geturl(url,dst)

    def geturl(self, url, dst):
        """retreives firmware bin, must use ATOM id for dst source."""
        urllib.urlretrieve(url, dst, self._reporthook)

    def _reporthook(self, numbcacheks, bcacheksize, filesize):
        """implements callback function for urllib2 to report progress. """
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
    """implements interface to FirmCache to be used by main program.

    Communicated with ThreadUrl using queue. """
    def __init__(self, signal, done):
        """Creates a simple cacheing for firmwares. """
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
        """Uses an ATOM entry to retreive firmware cache. """

        # src
        url = item['links'][0]['href']
        pdate = item['updated_parsed']

        # 'tag:boPunk,2009-01-12:/manual/id0'
        idpath = item['id'].split(':')[-1]
        id = os.path.join(*idpath.split('/'))
        dst = os.path.join( self.cache, id+'.bin' )

        self.queue.put((pdate, url, dst, done_sig))


    def clear(self):
        """clears cache using rmtree (carefule!). """
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
