import os, sys
sys.path.insert(0,os.path.join('.','src'))
from distutils.core import setup
import py2exe
# import BoPunkMainWindow, FirmwareFeed, FirmwareProxy
# import FirmwareTableModel, firmcache, urlcache
# import email, feedparser
# import email.Generator, email.Iterators, email.Message, email.Utils
  
import string,time,sys,os,smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import Encoders
from email import Message

# ['chardet', 'chardet.constants', 'cjkcodecs.aliases', 
# 'email.Generator', 'email.Iterators', 'email.Message', 'email.Utils', 
# 'iconv_codec', 'mx.Tidy', 'tidy']

setup(console=[ {"script" : "src/mainwindow.py"} ], 
    options={ "py2exe" : {
        "includes" : [
            "sip",
            "PyQt4.Qt",
            'email',
            'BoPunk'
    ],
        "packages" : [
            # 'tidy',
        ],
    }}
)