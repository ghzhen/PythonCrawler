#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib as ul

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(urlname):
  uf = ul.urlopen(urlname)
  texts = uf.read()

  imgfind = re.search(r'"image":"(.+)","name":',texts)
  if imgfind:
    imgurl = imgfind.group(1)
    img_url = imgurl.replace('\\','')
    print 'Image URL: ' + img_url    
  else:
    print 'Image URL: Not Found' 

  begstr = r'"name":"'
  bgnidx = texts.index(begstr)
  bgnidx += len(begstr)
  endstr = '"'
  endidx = texts.index(endstr, bgnidx)
  img_name = texts[bgnidx:endidx]
  print 'Image name: ' + img_name

  return img_url, img_name

def download_images(img_url, img_name, dest_dir):
  img_name = img_name.replace(' ','_') 

  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)
    print 'Create saving directory ' + dest_dir

  localpath = os.path.join(dest_dir, img_name)
  ul.urlretrieve(img_url, localpath)

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] urladdr '
    sys.exit(1)

  todir = '.'
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]
  urladdr = args[0]

  (img_url, img_name) = read_urls(urladdr)

  download_images(img_url, img_name, todir)

if __name__ == '__main__':
  main()
