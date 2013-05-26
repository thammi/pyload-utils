#!/usr/bin/env python3

import sys
import re

from pyloadutils.pyload import PyloadConnection

regex = re.compile('http://uploaded.\w+/404')

def main():
    con = PyloadConnection()

    packages = con.getQueueData()

    for package in packages:
        offline = [link for link in package['links'] if regex.match(link['url'])]

        if len(offline):
            print("Deleting %d files in %s" % (len(offline), package['name']))
            con.deleteFiles(fids=[link['fid'] for link in offline])

if __name__ == '__main__':
    sys.exit(main())
