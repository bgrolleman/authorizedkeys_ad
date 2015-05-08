ssh\_ad\_keys.py is used to fetch public ssh keys from active directory and keep a local
cache in case the AD isn't available.

## Install

Make sure the script is setup owned by the root user and that all parent directories are
from the root user as well. Directories/Executables need to be 0755 and files should be 0644

Create a local user to run the scripts, this should be a none privileged user that only has
access to the database file used for cache. It should never be allowed to change the lookup
script itself

Add the following to the sshd\_config

```
AuthorizedKeysCommand <Full path to script>
AuthorizedKeysCommandUser <User to run script>
```

cp the ssh\_ad\_keys.cfg.example file to /etc/ssh\_ad\_keys.cfg or next to the script and
setup the right variables. Check the config example for details

## Test script by hand

As the user running the script, start with a simple connect 

./ssh\_ad\_keys.py testad

Now try fetching a user from AD in debug mode

./ssh\_ad\_keys.py -d -u <USER> fetch

And test in production mode

./ssh\_ad\_keys.py <USER>

If you want you can update the .cfg file to set a bogus AD ip and test timeout. 

## Finalize setup

Restart sshd daemon and try remote login

## Links
* Fetch AD Data using LDAP - http://jrwren.wrenfam.com/blog/2006/11/17/querying-active-directory-with-unix-ldap-tools/
* Technet on link ssh to AD - https://social.technet.microsoft.com/Forums/en-US/8aa28e34-2007-49fe-a689-e28e19b2757b/is-there-a-way-to-link-ssh-key-in-ad?forum=winserverDS
* Discussion on logging in with SSH using AD as authentication - http://www.linuxquestions.org/questions/linux-enterprise-47/logging-in-via-ssh-while-authenticating-against-active-directory-618885/
* sshd authorizedkeyscommand - http://www.sysadmin.org.au/index.php/2012/12/authorizedkeyscommand/


