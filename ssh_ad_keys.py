#!/usr/bin/env python
#
# Description: Fetch Public SSH Keys from Active Directory
# Author: Bas Grolleman <bgrolleman@emendo-it.nl>
#
### Variables ###
# We want to move these to a configuration file
description = 'Fetch Public SSH Keys from Active Directory'

### Import Libs ###
import argparse
import sys
import ldap
import ConfigParser

### Fetch Configuration ###
config = ConfigParser.ConfigParser()
config.read(['ssh_ad_keys.cfg','/etc/ssh_ad_keys.cfg'])
ad_server = config.get('ad','server')
ad_port = config.get('ad','port')
ad_user = config.get('ad','user')
ad_password = config.get('ad','password')
ad_base = config.get('ad','base')

### Log Function ###
def log(line):
  if ( debug ):
    print line

### Connect to Active Directory Using LDAP ###
def connect():
  ad = ldap.initialize('ldap://%s:%s' % (ad_server,ad_port))
  ad.set_option(ldap.OPT_REFERRALS, 0)
  log(ad.simple_bind_s(ad_user,ad_password))
  return ad


### Authentication Mode ###
def auth():
    log('Authentication Mode')

### Update Mode ###
def update():
    log('Update Mode')

### Fetch Mode ###
def fetch():
    log('Fetch Mode')
    ad = connect()
    log('  Search Filter (&(objectClass=user)(sAMAccountName=%s))' % args.user[0])
    results = ad.search_s(ad_base,ldap.SCOPE_SUBTREE,filterstr='(&(objectClass=user)(sAMAccountName=%s))' % args.user[0])
    print results[0][1]['altSecurityIdentities']

### Test AD Mode ###
def testad():
    log('Test AD Mode')
    log('Connecting to %s' % ad_server)
    ad = connect()
    log(ad)

### Parse Agruments ###
parser = argparse.ArgumentParser(description = description)
parser.add_argument('--debug','-d', dest='debug', help="Enable Debug Messages", action='store_const', const=1, default=0)
parser.add_argument('--user','-u',dest='user',help="User to fetch from AD",action='store', nargs = 1)
parser.add_argument('--ad','-a',dest='ad',help="LDAP URL of Active Directory",action='store', nargs = 1)
parser.add_argument('mode', choices=['auth','update','fetch','testkeys','testad'])
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
