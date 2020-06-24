#!/usr/bin/python3

import configparser
import socket
import requests
import json

# Read and Parse the confg file
config = configparser.ConfigParser()
config.read('ddns.ini')

# API Endpoint for cPanel API2
URL = config['cpanel']['server'] + ':' + config['cpanel']['port'] + config['cpanel']['api']

DOMAIN = config['domain']['domain']
SUBDOMAIN = config['domain']['subdomain']
FQDN = SUBDOMAIN+"."+DOMAIN

# What is my current actual IP address
MYIP = json.loads(requests.get("https://httpbin.org/ip").text)['origin']

# What is the IP address currently set in DNS
DNSIP = socket.gethostbyname(FQDN)

# If they don't match then update DNS via the cPanel API
if MYIP != DNSIP:
    authparams = (
        config['cpanel']['username'],
        config['cpanel']['password']
    )

    # Call ZoneEdit::fetchzone to get the full zone file for DOMAIN
    fetchparams = (
        ('api.version', '2'),
        ('cpanel_jsonapi_module', 'ZoneEdit'),
        ('cpanel_jsonapi_func', 'fetchzone'),
        ('domain', DOMAIN),
    )

    response = requests.get(URL, auth=authparams, params=fetchparams)
    zonefile = json.loads(response.text)

    # Read each record looking for the sub domain we want to update
    for i, r in enumerate(zonefile['cpanelresult']['data'][0]['record']):
        if 'name' in list(r) and r['name'] == FQDN+".":
                editparams = (
                ('api.version', '2'),
                ('cpanel_jsonapi_module', 'ZoneEdit'),
                ('cpanel_jsonapi_func', 'edit_zone_record'),
                ('domain', DOMAIN),
                ('line', r['line']),
                ('name', r['name']),
                ('type', r['type']),
                ('address', MYIP),
                )
            
                response = requests.get(URL, auth=authparams, params=editparams)
