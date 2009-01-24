import os
from urllib import quote, unquote
import urllib2
import email
import email.iterators, email.generator, email.message

from StringIO import StringIO
import hashlib, shutil

VERSION="1.1-modified"

class CachedResponse(StringIO):
    def info(self):
        return self.headers

    def geturl(self):
        return self.url

    def getfile(self):
        return self.fp
    
    def getpath(self):
        return self.path
    

class CachedHandler(urllib2.BaseHandler):
    """
    """
    def __init__(self, cache, debug=0):
        self._debug = debug
        if not os.path.isdir(cache):
            try:
                # print("Creating firmware cache")
                os.mkdir(cache)
            except os.OSError, inst:
                print("FirmCache: Couldn't Create cache: ERROR:", inst)
                raise AppError(exit=True)
        self.cache = cache
    
    def default_open(self, request):
        if request.get_method() != 'GET':
            return None
        full = request.get_full_url()
        url = quote(full, '')
        path = os.path.join(self.cache, url)
        
        if self._debug:
            print("default_open: request", request.get_full_url())
            print("default_open: url", url)
            print("default_open: path", path)
        
        if os.path.exists(path):
            f = open(path)
            data = email.message_from_file(f)
            if data.get('x-cache-md5') is None:
                return None
            payload = data.get_payload()
            if data.get('x-cache-md5') != hashlib.md5(payload).hexdigest():
                return None
            response = CachedResponse(payload)
            response.url = full
            response.headers = dict(data.items())
            response.fp = response
            response.path = f.name
            try:
                response.code = int(data['x-cache-code'])
                response.msg = data['x-cache-msg']
            except (TypeError, KeyError):
                return None
            return response
        elif full.startswith("file://"):
            # copy to local directory and create response object
            shutil.copyfile(full[7:],path)
            # try just calling self again to get object
            response = open(path)
            return response
        else:
            return None

    def http_response(self, request, response):
        if request.get_method() != 'GET':
            return response
        headers = response.info()
        if headers.get('x-cache-md5') == None:
            data = email.message.Message()
            for k,v in headers.items():
                data[k] = v
            payload = response.read()
            data['x-cache-md5'] = hashlib.md5(payload).hexdigest()
            data['x-cache-code'] = str(response.code)
            data['x-cache-msg'] = response.msg
            data.set_payload(payload)
            url = quote(request.get_full_url(), '')
            path = os.path.join(self.cache, url)
            try:
                f = open(path, 'wb')
                f.write(str(data))
                f.flush()
                f.close()
            except IOError, inst:
                print("inst", inst)
                raise inst
            new_response = CachedResponse(payload)
            new_response.url = response.url
            new_response.headers = response.headers
            new_response.code = response.code
            new_response.msg = response.msg
            new_response.fp = new_response
            new_response.path = f.name
            
            return new_response
        return response
    
    def clear(self):
        shutil.rmtree(self.cache)
        os.mkdir(self.cache)



def build_opener(cache):
    return urllib2.build_opener(CachedHandler(cache))
    


    
if __name__ == '__main__':    
    pass
    
    
    