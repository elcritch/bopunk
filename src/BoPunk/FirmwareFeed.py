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
if __name__ == "__main__":
    import os, sys
    sys.path.append("../")

import BoPunk.lib.feedparser as feedparser
from Settings import *
# import uuid
import encodings
import lib.imp_all_encodings
import socket, time
"""
import urllib
>>> opener = urllib.FancyURLopener({})
>>> f = opener.open("http://www.python.org/")
>>> f.read()
"""

def createLocalItem(feed, path, item_dict={}):
    """Function to create a manual firmware feed item.

    Args:
    feed -- FirmwareFeed to be used for parent.
    path -- url location.
    item_dict -- item dictionary to add to default feed item. Default = {}.
    """
    path = os.path.abspath(path)
    item = FeedItem(feed, path)
    
    loc_dt = time.gmtime(os.path.getmtime(path))
    
    item.elem = {
        'title':"Manual Firmware %i"%len(feed.feed_manual()),
        'id':'tag:boPunk,2009-01-12:/manual/id%d'%len(feed.feed_manual()),
        'summary':'',
        # 'published':'2005-11-10T00:23:47Z',
        'updated':'2005-11-11T11:56:34Z',
        'updated_parsed': loc_dt,
        'author':"",
        'content':[{
            'value':"""
                <html>
                    <h1>Local Firmware</h1><br>
                    <bold>From File: </bold>%s<br>
                    <bold>Resource: </bold><!--RES--><br>
                </html>"""%(path)}],
        'links':[
            {'href':"file://%s"%path},
        ]
    }
    item.elem.update(item_dict)
    item.islocal = True
    return item


class FirmwareFeed:
    """Parses atom feeds into a python data structure and stores the resulting data."""

    def __init__(self, url = "../test/firms.atom.xml", mainwindow=None):
        """Takes a file/url atom feed and parses it. """
        self._url = url
        self._items_manual = list()

        # change default global socket timeout
        timeout = 4
        socket.setdefaulttimeout(timeout)

        # try retreiving url
        self.refresh(url)



    def refresh(self, path=None):
        """Refreshes RSS list. """
        print "Refreshing feed"
        location = path if path else self._url

        self._feed = feedparser.parse(location)

        # TODO: add intelligent error handling
        if self._feed.has_key('bozo_exception'):
            self._feed['entries'] = [] # set to empty

        self._items = [ FeedItem(self, i) for i in self._entries() ]

    def _entries(self):
        """Private method to return list of entries from a feed."""
        return self._feed['entries']

    def addManualItem(self, item):
        """Adds a manually created firm item entry."""
        self._items_manual.append(item)

    def delManualItem(self, item):
        """Removes a manually created firm item entry."""
        idx = self.find(item['id'])
        idx = idx - len(self.feed_items())
        return self._items_manual.pop(idx)
    
    def __delManualUrl(self, url):
        """Removes a manually firm item entry using input file name."""
        for i, item in enumerate(self._items_manual):
            if item['links'][0]['href'] == url:
                return self._items_manual.pop(i)

    def item(self, idx):
        """returns item with given index, raise IndexError if not found."""
        return self.__getitem__(idx)

    def items(self):
        """returns combined list of feed items and manual items. """
        return self._items+self._items_manual

    def feed_items(self):
        """returns only feed items. """
        return self._items

    def feed_manual(self):
        """returns only manual items. """
        return self._items_manual

    def __len__(self):
        """returns total length of feed and manual items. """
        return len(self._items_manual)+len(self._items)

    def __getitem__(self,idx):
        """implements getitem interface, returns given item for the index.

        The index starts from 0 for feed items. Manual items are indexed after
        fedd items.
        """
        size = len(self)
        if not isinstance(idx, int): raise TypeError("index must be an int")

        if idx < len(self._items):
            return self._items[idx]
        elif idx < size:
            return self._items_manual[idx%len(self._items)-1]
        else:
            raise IndexError("Index incorrect of list is empty: %i"%idx)

    def find(self, atomid):
        """Finds a firmware (if present) for a given atom id. """
        for i in range(len(self)):
            item = self.item(i)
            if item['id'].endswith(atomid):
                return i


class FeedItem:
    """Wrapper for FeedParser entries. """
    def __init__(self, parent, elem, path = None):
        """create a wrapper for an atom elem entry. """
        self.elem = elem
        self.parent = parent
        self._path = path
        self.islocal = False


    def getPath(self):
        """returns path (if any) of firmcache. """
        return self._path

    def get(self, key):
        """returns data in feed entry for a given key which is lowercased. """
        return self.elem[key.lower()]

    def getContent(self, row = 0, name='src'):
        """returns url of firmware description.

        Used in MainWindow to update description paine. """
        item = self.elem['content'][row]

        if name == 'src' and item.has_key('base'):
            return item['base']+item['src']
        else:
            return item[name]

    def __getitem__(self, key):
        """returns entry data for a key after lowercasing it. """
        return self.elem.get(key.lower())
    def __getattr__(self, name):
        """provides attribute based access to entry data elements. """
        # print "name '%s' '%s' "%(type(name), name),
        return self.elem.get(name)
    def __repr__(self):
        """return repr() of entry. """
        return repr(self.elem)
    def __str__(self):
        """return str() of entry. """
        return str(self.elem)

if __name__ == "__main__":
    global atom
    import os, sys
    sys.path.append("../")
    # ex = feedparser.parse("../test/atom10.xml")
    url = "http://www.bocolab.org/bopunks/feeds/firms.atom.xml"
    atom = FirmwareFeed(url)

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
