# ssh_ad_keys script

## Goal
Script to check AD Public SSH Keys and keep a local cached copy

## Functions

### Authenticate

Try to connect to AD and fetch all available keys for user, if connection takes more then
2 seconds then timeout and fetch keys from local sqllite.db file 

### Update

Connect to AD to fetch all public keys and update sqllite.db file, also use private key to
generate matching signature file. 

### Fetch

Get sqllite.db file from central location and after downloading it compare the signature
with local key to make sure the original was properly generated. This function is mostly
for scale and to avoid every machine hammering the AD every hour

### TestKeys

Simply return the keys in test_keys file, used to debug SSH Login

### TestAd

Simply return public keys for specific user, used to debug AD connection

