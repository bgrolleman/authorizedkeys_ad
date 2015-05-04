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
import sqlite3
import os

### Fetch Configuration ###
workdir = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser({
  'port': '389',
  'dbfile': '%s/ssh_ad_keys.db' % workdir
})
config.read(['%s/ssh_ad_keys.cfg' % workdir,'/etc/ssh_ad_keys.cfg'])
ad_server = config.get('ad','server')
ad_port = config.get('ad','port')
ad_user = config.get('ad','user')
ad_password = config.get('ad','password')
ad_base = config.get('ad','base')
db_dbfile = config.get('db','dbfile')
db = sqlite3.connect(db_dbfile)
db.execute('create table if not exists cached_keys ( date text, user text, key text )')

### Log Function ###
def log(line):
  if ( debug ):
    print line

### Connect to Active Directory Using LDAP ###
def connect():
  ad = ldap.initialize('ldap://%s:%s' % (ad_server,ad_port))
  ad.set_option(ldap.OPT_REFERRALS, 0)
  ad.set_option(ldap.OPT_NETWORK_TIMEOUT, 2.0)
  log(ad.simple_bind_s(ad_user,ad_password))
  return ad

### Fetch Mode ###
def fetch(user):
    # Check if user has domain and strip it
    if ( user.find('+') > 0 ):
      user = user.split('+')[1]
    log('Fetch Mode')
    ad = connect()
    log('  Search Filter (&(objectClass=user)(sAMAccountName=%s))' % user)
    results = ad.search_s(ad_base,ldap.SCOPE_SUBTREE,filterstr='(&(objectClass=user)(sAMAccountName=%s))' % user)
    for result in results:
      if result[0]:
        log(result)
        keys = results[0][1]['altSecurityIdentities']
        for key in keys:
          if key.startswith('SSHKey:') or key.startswith('sshPublicKey'):
            key = key.replace('SSHKey:','',1)
            key = key.replace('sshPublicKey:','',1)
            print key
    sys.exit(0)

### Test AD Mode ###
def testad():
    log('Test AD Mode')
    log('Connecting to %s' % ad_server)
    ad = connect()
    log(ad)

### Parse Agruments ###
parser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description = '''Fetch Public SSH Keys from Active Directory

Operating Modes
  fetch	      This fetches the Public Keys for the user provided with the --user argument
  testad      Only connect to AD, used to test connection.
''')
parser.add_argument('--debug','-d', dest='debug', help="Enable Debug Messages", action='store_const', const=1, default=0)
parser.add_argument('--user','-u',dest='user',help="User to fetch from AD",action='store', nargs = 1)
parser.add_argument('--ad','-a',dest='ad',help="LDAP URL of Active Directory",action='store', nargs = 1)
parser.add_argument('mode', choices=['fetch','testad'])

# AuthorizedKeysCommand Compatibility mode
if ( len(sys.argv) == 2 ):
  if not sys.argv[1].startswith('-') and not sys.argv[1] == 'testad':
    debug = 0
    fetch(sys.argv[1])
    sys.exit(0)

# More arguments then parse
args = parser.parse_args()
debug = args.debug
log('Debug enabled')
if ( len(sys.argv) == 1 ):
    parser.print_help()

if(args.mode == 'fetch'):
    fetch(args.user[0])
if(args.mode == 'testad'):
    testad()
