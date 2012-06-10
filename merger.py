#!/usr/bin/env python3

from os.path import expanduser

from urllib.request import urlopen
from urllib.parse import urljoin, urlencode

from configparser import ConfigParser

import json

import re

import sys

class PyloadConnection:

    def __init__(self):
        config = ConfigParser()
        config.read(expanduser("~/.pyload_merge"))

        self.url_base = urljoin(config.get('base', 'host'), 'api/')

        user = config.get('base', 'user')
        password = config.get('base', 'password')

        self.session = None
        self.session = self._call('login', {'username': user, 'password': password}, False)

    def _call(self, name, args={}, encode=True):
        url = urljoin(self.url_base, name)

        if encode:
            data = {}

            for key, value in args.items():
                data[key] = json.dumps(value)
        else:
            data = args

        if self.session:
            data['session'] = self.session

        post = urlencode(data).encode('utf-8')

        return json.loads(urlopen(url, post).read().decode('utf-8'))

    def __getattr__(self, name):
        def wrapper(**kargs):
            return self._call(name, kargs)

        return wrapper

def main():
    con = PyloadConnection()

    collected = con.getCollectorData()

    bags = {}

    regex = re.compile(sys.argv[1] if len(sys.argv) > 1 else '.*')

    for package in collected:
        match = regex.match(package['name'])

        if match:
            if match.groups():
                part = match.group(1)
            else:
                part = match.group(0)

            if part in bags:
                bags[part].append(package)
            else:
                bags[part] = [package]

    for key, packages in list(bags.items()):
        if len(packages) > 1:
            def count_finished(package):
                count = 0

                for link in package['links']:
                    if link['status'] == 0:
                        count += 1

                return count

            packages.sort(key=count_finished, reverse=True)
        else:
            del bags[key]

    for key, packages in list(bags.items()):
        print(key)

        for package in packages:
            files = len(package['links'])
            hosters = set(link['plugin'] for link in package['links'])
            print("- %s (%i files; %s)" % (package['name'], files, ', '.join(hosters)))

        print()

    if not bags:
        print("Nothing to merge")
        return

    accept = input("Do you want to merge these packages? ")

    if accept not in ['y', 'j']:
        print("OK, aborting!")
        return

    print()

    for key, packages in bags.items():
        print("Merging", key, "...")

        root = packages[0]
        rest = packages[1:]

        pid = root['pid']

        if root['name'] != key:
            con.setPackageName(pid=pid, name=key)

        links = []

        for package in rest:
            links += (link['url'] for link in package['links'])

        con.addFiles(pid=pid, links=links)

        pids = [package['pid'] for package in rest]

        con.deletePackages(pids=pids)


if __name__ == '__main__':
    sys.exit(main())
