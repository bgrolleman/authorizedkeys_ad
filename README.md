## ssh_ad_keys.py README

`ssh_ad_keys.py` is used to fetch public ssh keys from active directory and keep a local cache in case the AD isn't available.

## Dependencies
* python-ldap
* python-sqlite
* ssh v6.6p1 or higher
* OpenBroker

## Install

### Directories and Permissions
It's best to install the script in /opt/authorizedkeys_ad and make sure that ownership and writability is set to `root` only. Ownership of the files and the executable should be `0755` 

Please note that you should configure a dedicated user to run the script that can only write in /var/cache/ssh_ad_keys, this is used to write the sqlite database

All these directories can be configured, so keep special setup's in mind and make sure to check the ssh_ad_keys.cfg file

### User

Create a local user to run the scripts, this should be a none privileged user that only has access to the database file used for cache. It should never be allowed to change the lookup script itself.

I recommend the user is called `ssh_ad_keys`, with home directory set to `/var/cache/ssh_ad_keys`

Create the user using 

    adduser --system --home /var/cache/ssh_ad_keys ssh_ad_keys

Add the following to `/etc/ssh/sshd_config`

    AuthorizedKeysCommand /opt/authorizedkeys_ad/ssh_ad_keys.py
    AuthorizedKeysCommandUser ssh_ad_keys

### Configuration File
Copy the `ssh_ad_keys.cfg.example` file to `/etc/ssh_ad_keys.cfg` or next to the script and setup the right variables. Check the config example for details.

## Test script by hand

As the user running the script, start with a simple connect 

   ./ssh_ad_keys.py testad

Now try fetching a user from AD in debug mode, this shows extra details on the user being fetched

    ./ssh_ad_keys.py -d -u USERNAME fetch

Finally test the script as it is used by ssh daemon, it should now only return the keys

    ./ssh_ad_keys.py USERNAME

Finally you could update the .cfg to a fake IP and cache should work now. Still resulting in the right key being returned

## Finalize setup

Restart sshd daemon and try remote login

    /etc/init.d/ssh restart

## Links

* Fetch AD Data using LDAP - http://jrwren.wrenfam.com/blog/2006/11/17/querying-active-directory-with-unix-ldap-tools/
* Technet on link ssh to AD - https://social.technet.microsoft.com/Forums/en-US/8aa28e34-2007-49fe-a689-e28e19b2757b/is-there-a-way-to-link-ssh-key-in-ad?forum=winserverDS
* Discussion on logging in with SSH using AD as authentication - http://www.linuxquestions.org/questions/linux-enterprise-47/logging-in-via-ssh-while-authenticating-against-active-directory-618885/
* sshd authorizedkeyscommand - http://www.sysadmin.org.au/index.php/2012/12/authorizedkeyscommand/

## FAQ

### I keep getting exit with 1 messages in my auth.log
Try running the command by hand as the user configured in sshd, use the -d switch to get more debug info.
Most of the time it can't write to the DB cache file, make sure the /var/cache/ssh_ad_keys directory is owned by the user running the script and that the .db file is removed.

### I get write errors for the db file
It should be owned user/group by the user running the script, so previous FAQ on how to fix this

### Login/Password failures
Always make sure to check if password login works, if this fails then you might need to inspect powerbroker

