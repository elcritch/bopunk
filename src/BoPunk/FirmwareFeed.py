"""
Class for parsing a Firmware plist info and holding the resulting python data
structure

Author: Jarremy Creechley
License: See License.txt for more details

Copyright (C) 2009 Jaremy Creechley <creechley@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import BoPunk.lib.feedparser as feedparser
from Settings import *
# import uuid
import encodings
import lib.imp_all_encodings
import socket
"""
import urllib
>>> opener = urllib.FancyURLopener({})
>>> f = opener.open("http://www.python.org/")
>>> f.read()
"""

def createLocalItem(parent, loc, resource, item_dict={}):
    item = FeedItem(parent, loc)
    item.elem = {
        'title':"Manual Firmware %i"%len(parent.feed_manual()),
        'id':'tag:boPunk,2009-01-12:/manual/id0',
        'summary':'',
        'published':'2005-11-10T00:23:47Z',
        'updated':'2005-11-11T11:56:34Z',        
        'author':"", 
        'content':[{
            'value':"""
                <html>
                    <h1>Local Firmware</h1><br>
                    <bold>From File: </bold>%s<br> 
                    <bold>Resource: </bold>%s<br> 
                </html>"""%(loc,resource)}],
        'links':[
            {'href':"file://%s"%loc},
        ]
    }
    item.elem.update(item_dict)
    item.islocal = True
    return item


class FirmwareFeed:
    """
    Parses atom feeds into a python data structure and stores the resulting data
    """
    
    def __init__(self, url = "../test/firms.atom.xml", mainwindow=None):
        """Takes a file/url atom feed and parses it."""
        self._url = url
        self._items_manual = list()
        
        # change default global socket timeout
        timeout = 4
        socket.setdefaulttimeout(timeout)
        
        # try retreiving url
        self.refresh(url)
        
        
        
    def refresh(self, loc=None):
        """refreshes RSS list"""
        print "Refreshing feed"
        location = loc if loc else self._url
        
        self._feed = feedparser.parse(location)
        
        # TODO: add intelligent error handling
        if self._feed.has_key('bozo_exception'):
            self._feed['entries'] = [] # set to empty
            
        self._items = [ FeedItem(self, i) for i in self._entries() ]
    
    def _entries(self):
        return self._feed['entries']
    
    def addManualItem(self, item):
        self._items_manual.append(item)
    
    def item(self, idx):
        return __getitem__(idx)
        
    def items(self):
        return self._items+self._items_manual
    
    def feed_items(self):
        return self._items
        
    def feed_manual(self):
        return self._items
    
    def __len__(self):
        return len(self._items_manual)+len(self._items)
    
    def __getitem__(self,idx):
        size = len(self)
        if not isinstance(idx, int): raise TypeError("index must be an int")
        
        if idx < len(self._items):
            return self._items[idx]
        elif idx < size:
            return self._items_manual[idx%len(self._items)-1]
        else:
            raise IndexError("Index incorrect of list is empty: %i"%idx)
        
    
    
    

class FeedItem:
    
    def __init__(self, parent, elem, loc = None):
        """create a wrapper for an atom elem entry"""
        self.elem = elem
        self.parent = parent
        self._path = loc
        self.islocal = False
        
                
    def getPath(self):
        return self._path
    
    def get(self, key):
        """Returns elem for given key"""
        return self.elem[key.lower()]
    
    def getContent(self, row = 0, name='src'):
        item = self.elem['content'][row]
        
        if name == 'src' and item.has_key('base'):
            return item['base']+item['src']
        else:
            return item[name]
    
        
    def __getitem__(self, key):
        return self.elem.get(key.lower())
    
    def __getattr__(self, name):
        # print "name '%s' '%s' "%(type(name), name), 
        return self.elem.get(name)
    
    def __str__(self):
        return str(self.elem)

if __name__ == "__main__":
    global atom
    
    # ex = feedparser.parse("../test/atom10.xml")   
    loc = "http://192.168.1.101/~jaremy/bopunk/feeds/firms.atom.xml"
    atom = FirmwareFeed(loc)
    
    print "type(atom._entries())", type(atom._entries())
    print "atom._entries", len(atom._entries())
    print "atom[0].author", atom[0].author    
    
    print "type(atom.items())", type(atom.items())
    print "type(atom[0])", type(atom[0].elem)
    print "atom[0]", atom[0]
    
    print "\n"
    
    
    for item in atom:
        print "\nITEM", item.title, item.author, item.summary
        print "content:", item.getContent()