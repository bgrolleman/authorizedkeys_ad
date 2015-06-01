# Setup SSH AD on Ubuntu 12.04

Step by Step Instructions run on Ubuntu 12.04, this is almost shell script except for a few manual steps and the creation of the conifg file. 

Please note that the IPs/Logins used in here are fake and will not work out of the box, they need to be updated

## Install OpenSSH 6.6 (Only on 12.04, do check version on 14.04)
    sudo -s -H
    cd /root
    apt-get update
    apt-get install -y zlib1g-dev libssl-dev libpam-dev
    wget http://mirror.aarnet.edu.au/pub/OpenBSD/OpenSSH/portable/openssh-6.6p1.tar.gz
    tar zxf openssh*.tar.gz
    cd openssh-6.6p1
    ./configure --prefix=/usr -sysconfdir=/etc/ssh --with-md5-passwords --with-privsep-path=/var/lib/sshd --with-pam
    make
    make install
    /etc/init.d/sshd restart

## Install OpenBroker
    cd /root
    wget http://download.beyondtrust.com/PBISO/8.1.1/linux.deb.x64/pbis-open-8.1.1.2469.linux.x86_64.deb.sh
    bash pbis*sh
    # Legacy Links no, install now yes
    sed -i 's/192.168.0.8/192.168.0.68/' /etc/resolv.conf
    domainjoin-cli join testduomfa-rakops.com Administrator
    # Should return SUCCESS, make sure to have administrator password at hand
    /opt/pbis/bin/config HomeDirTemplate %H/%D/%U
    /opt/pbis/bin/config AssumeDefaultDomain false
    /opt/pbis/bin/config DomainSeparator +
    /opt/pbis/bin/config RequireMembershipOf TESTDUOMFA-RAKO+testduo
    /opt/pbis/bin/config LoginShellTemplate /bin/bash

## Install Public key script
    apt-get install -f git
    cd /opt
    git clone https://github.com/bgrolleman/authorizedkeys_ad.git
    cd authorizedkeys_ad
    apt-get install -f python-ldap
    # Create /opt/authorizedkeys_ad/ssh_ad_keys.cfg
    adduser --system --home /opt/authorizedkeys_ad ssh_ad_keys
    mkdir /var/cache/ssh_ad_keys
    chown ssh_ad_keys /var/cache/ssh_ad_keys
    # Should return key of test.test user
    /opt/authorizedkeys_ad/ssh_ad_keys.py test.test

## Configure SSHD
    echo "AuthorizedKeysCommandUser ssh_ad_keys" >> /etc/ssh/sshd_config
    echo "AuthorizedKeysCommand /opt/authorizedkeys_ad/ssh_ad_keys.py" >> /etc/ssh/sshd_config
    /etc/init.d/ssh restart

### Check Settings
Use this as a first check when auth.log shows script returned with 1, this also clears the public key cache
    chown root /opt
    chown -R root /opt/authorizedkeys_ad
    chown ssh_ad_keys /var/cache/ssh_ad_keys
    rm /var/cache/ssh_ad_keys/*

## ssh_ad_keys.cfg
    [ad]
    server: 192.168.0.68
    user: TEST-DOMAIN\Administrator
    password: *secret*
    base: dc=test-domain,dc=com

    [db]
    dbfile: /var/cache/ssh_ad_keys/ssh_ad_keys.db
    cache_timeout: -3 months

## Double check if not working
* ssh -V returns version 6.6 or higher?
* Make sure you can login with password, if not check ssh compile switches and power broker install
* The script and all it's parent directories must be owned by root and not writable by anyone else
* The /var/cache/ssh_ad_keys directory must be writable by ssh_ad_keys as well as the .db file there
