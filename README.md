# cpanel-ddns

A python script that uses the latest cPanel API 2 to update cPanel zone files so you can use your cPanel account for Dynamic DNS.

You'll need to create your own ddns.ini file with your cPanel url, and your username & password.

Your main domain (eg. example.com) and the sub domain whose A-record you want to update (eg. www) also go in the .ini file.
