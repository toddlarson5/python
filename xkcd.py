#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 12:58:57 2017

@author: toddlarson
"""

import requests
import bs4
import sys
import re
import os


def main():
    if not os.path.isdir('./xkcd'):
        os.makedir('xkcd', exist_ok=True)

    os.chdir('./xkcd')
    baseLink = 'http://www.xkcd.com'
    prevLink = ''

    # The first ever xkcd comic's previous link is '#'
    while prevLink != '#':
        prevLink = downloadImage(baseLink + prevLink)

# Fuction returns previous xkcd comic address
def previousLink(soup):
    # Find previous link
    prev = soup.select('a[rel="prev"]')[0]
    return prev.get('href')

# Function downloads xkcd comic image file
def downloadImage(link):
    res = requests.get(link)
    try:
        res.raise_for_status()
    except Exception as e:
        print('There was a problem contacting xkcd.com:{}'.format(e))
        sys.exit()

    comicSoup = bs4.BeautifulSoup(res.text)
    results = comicSoup.select('#comic img')

    # Skips XKCD comic 1663 since it is not an image
    if results == []:
        return previousLink(comicSoup)

    link = results[0].get('src')
    name = results[0].get('alt')

    # Skips XKCD comic number 1525 since it is not an image
    if name is None:
        return previousLink(comicSoup)

    # Removes forward slashes from the comic name
    forwardSlash = re.compile(r'/')
    if forwardSlash.search(name) is not None:
        name = forwardSlash.sub(' ', name)

    comicFile = open(name + '.png', 'wb')
    res = requests.get('http:' + link)

    try:
        res.raise_for_status()
    except Exception as e:
        print('There was a problem downloading image:{}'.format(e))

    for chunk in res.iter_content(1000000):
        comicFile.write(chunk)

    comicFile.close()

    # Return previous comic link
    return previousLink(comicSoup)

if __name__ == "__main__":
    main()
