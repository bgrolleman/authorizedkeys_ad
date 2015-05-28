`ssh_ad_keys.py` is used to fetch public ssh keys from active directory and keep a local cache in case the AD isn't available.

## Dependencies

**TODO**

## Install

Make sure the script is setup owned by the root user and that all parent directories are from the root user as well. Directories/Executables need to be `0755` and files should be `0644`.

## Directories andPermissions

**TODO**

## User

Create a local user to run the scripts, this should be a none privileged user that only has access to the database file used for cache. It should never be allowed to change the lookup script itself

Add the following to `/etc/ssh/sshd_config`

```text
AuthorizedKeysCommand <Full path to script>
AuthorizedKeysCommandUser <User to run script>
```

Copy the `ssh_ad_keys.cfg.example` file to `/etc/ssh_ad_keys.cfg` or next to the script and setup the right variables. Check the config example for details.

## Test script by hand

As the user running the script, start with a simple connect 

```text
./ssh_ad_keys.py testad
```

Now try fetching a user from AD in debug mode

```text
./ssh_ad_keys.py -d -u <USER> fetch
```

And test in production mode

```text
./ssh_ad_keys.py <USER>
```

If you want you can update the .cfg file to set a bogus AD ip and test timeout. 

## Finalize setup

Restart sshd daemon and try remote login

```text
/etc/init.d/ssh restart
```

## Links

* Fetch AD Data using LDAP - http://jrwren.wrenfam.com/blog/2006/11/17/querying-active-directory-with-unix-ldap-tools/
* Technet on link ssh to AD - https://social.technet.microsoft.com/Forums/en-US/8aa28e34-2007-49fe-a689-e28e19b2757b/is-there-a-way-to-link-ssh-key-in-ad?forum=winserverDS
* Discussion on logging in with SSH using AD as authentication - http://www.linuxquestions.org/questions/linux-enterprise-47/logging-in-via-ssh-while-authenticating-against-active-directory-618885/
* sshd authorizedkeyscommand - http://www.sysadmin.org.au/index.php/2012/12/authorizedkeyscommand/

## FAQ

### I keep getting exit with 1 messages in my auth.log
Try running the command by hand as the user configured in sshd, use the -d switch to get more debug info

### I get write errors for the db file
It should be owned user/group by the user running the script
