#!/usr/bin/env python
"""Split an compare POST"""
__author__="Samuel COZANET <s.cozanet@jurismarches.com>"

import sys
import os.path
import subprocess
import urllib

def sortedDictValues2(adict):
    keys = adict.keys()
    keys = sorted(keys)
    data = {}
    for key in keys:
        data[key] = adict[key]
    return data

def compare(file1, file2):
    subprocess.call(["vimdiff", file1, file2])

def prepare(filename):
    content = u''
    for key, value in create_dict(filename).items():
        content += u'%s=%s\n' % (key, value)

    openfile = open(filename, 'w')
    openfile.write(content)
    openfile.close()

def create_dict(filename):
    content = file(filename).read()
    content = content.replace(u'&', u'\n')
    content = urllib.unquote_plus(content)
    postdata = {}
    for line in content.splitlines():
        var = line.split(u'=')
        if var[1]:
            postdata[var[0]] = var[1]
        else:
            postdata[var[0]] = u''

    return sortedDictValues2(postdata)


def create(filename):
    print create_dict(filename)

def print_help():
    print "Usage: %s [command]\n" % os.path.basename(sys.argv[0])
    print "Commands:"
    print "  compare  start an instance"
    print "  prepare  stop an instance"
    print "  create   create postdata dict"
    print "  help     show this help message"

COMMANDS = {
    'compare': compare,
    'prepare': prepare,
    'create' : create,
}

def main(command):
    if command in COMMANDS.keys():
        if command == 'compare':
            if len(sys.argv) == 4:
                COMMANDS.get(command)(sys.argv[2], sys.argv[3])
            else:
                print "Usage: %s compare [file_name1] [file_name2]\n" % os.path.basename(sys.argv[0])
        else:
            if len(sys.argv) == 3:
                COMMANDS.get(command)(sys.argv[2])
            else:
                print "Usage: %s prepare [file_name]\n" % os.path.basename(sys.argv[0])
                print "       %s create [file_name]\n" % os.path.basename(sys.argv[0])
    else:
        print_help()

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        print_help()
