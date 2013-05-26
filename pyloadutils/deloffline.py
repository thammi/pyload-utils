#!/usr/bin/env python3

import sys

from pyloadutils.pyload import PyloadConnection

def main():
    con = PyloadConnection()

    packages = con.getQueueData()

    for package in packages:
        offline = [link for link in package['links'] if link['status'] == 1]

        if len(offline) == 0:
            continue

        print("The following links in '%s' are offline:" % package['name'])

        for plugin in set(link['plugin'] for link in offline):
            plugin_links = len([link for link in offline if link['plugin'] == plugin])
            print("- %i links from %s" % (plugin_links, plugin))

            for i in set(l['statusmsg'] for l in offline):
                print(i)


        answer = input("Do you want to delete those links? ")

        print()

        if answer.lower() in ['y', 'yes', 'j', 'ja']:
            con.deleteFiles(fids=[link['fid'] for link in offline])

if __name__ == '__main__':
    sys.exit(main())
