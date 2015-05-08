20150314
Collecting information into a small git repository, planning time to dive into this

20150403
* Setup document about SSH Authorized Keys script
* Setup a small Vagrant box to test SSH login using the ssh command function
* Create Skeleton script for SSH Authentication
* Configure SSH to use authorizedkeyscommand
* This seems to break logging into the machine
* Log files are not showing any issues, going to enable debug on monday and dig a bit deeper

20150508
* Script is finished now
* Uses AD when possible, but switches to cache if unavailable
* Double check that the script is owned by root as well as all parent directories
* Make sure that the non privileged user running that script can read/write db


