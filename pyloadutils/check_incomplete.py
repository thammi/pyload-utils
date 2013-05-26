#!/usr/bin/env python3

import sys
import re

from pyloadutils.pyload import PyloadConnection

regex = re.compile('http://.*')

def main():
    con = PyloadConnection()

    packages = con.getQueueData()

    for package in packages:
        incomplete = [link for link in package['links'] if regex.match(link['name'])]

        if len(incomplete):
            print("Checking %s" % package['name'])
            con.recheckPackage(pid=package['pid'])

if __name__ == '__main__':
    sys.exit(main())
