#!/usr/bin/env python
#
# Description: Fetch Public SSH Keys from Active Directory
# Author: Bas Grolleman <bgrolleman@emendo-it.nl>
#
### Variables ###
# We want to move these to a configuration file
description = 'Fetch Public SSH Keys from Active Directory'
ad_server = 'localhost'

### Import Libs ###
import argparse
import sys

### Log Function ###
def log(line):
  if ( debug ):
    print line

### Authentication Mode ###
def auth():
    log('Authentication Mode')

### Update Mode ###
def update():
    log('Update Mode')

### Fetch Mode ###
def fetch():
    log('Fetch Mode')

### Test Keys Mode ###
def testkeys():
    log('Test Keys Mode')

### Test AD Mode ###
def testad():
    log('Test AD Mode')

### Parse Agruments ###
parser = argparse.ArgumentParser(description = description)
parser.add_argument('--debug','-d', dest='debug', help="Enable Debug Messages", action='store_const', const=1, default=0)
parser.add_argument('mode', choices=['auth','update','fetch','testkeys','testad'])
parser.add_argument('--user','-u',dest='user',help="User to fetch from AD",action='store', nargs = 1)
parser.add_argument('--ad','-a',dest='ad',help="LDAP URL of Active Directory",action='store', nargs = 1)
args = parser.parse_args()
debug = args.debug
log('Debug enabled')
if ( len(sys.argv) == 1 ):
    parser.print_help()

if(args.mode == 'auth'):
    auth()
if(args.mode == 'update'):
    update()
if(args.mode == 'fetch'):
    fetch()
if(args.mode == 'testkeys'):
    testkeys()
if(args.mode == 'testad'):
    testad()
