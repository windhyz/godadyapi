#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File Name: godaddylib.py
Author: windhyz
Mail: windhyz@139.com
Time: 2018-09-20
"""
try:
    import requests, json, argparse
except KeyboardInterrupt:
    pass

VERSION = '0.1.0'

class DodaddyDomain(object):

    def __init__(self, _id, _key, _secret, _url, godapihost):
        self.id = _id
        self.key = _key
        self.secret = _secret
        self.url = _url
        self.godapihost = godapihost

    def goddomain(self, key, secret, url, godapihost):

        headers = {"Accept": "application/json",
                   "Authorization": "sso-key %s:%s" % (key, secret)}
        _url = 'https://%s/%s' % (godapihost, url)

        try:
            ret = requests.get(_url, headers=headers)

        except requests.RequestException as e:
            errmsg = "request %s Failed: %s" % (_url, e)

        if ret.status_code == 200:
            return ret.status_code, json.loads(ret.text)
        else:
            return errmsg

    def goddomaindetail(self, key, secret, godapihost, url, subdomain):
        headers = {"Accept": "application/json",
                   "Authorization": "sso-key %s:%s" % (key, secret)}
        _url = 'https://%s/%s/%s' % (godapihost, url, subdomain)

        try:
            ret = requests.get(_url, headers=headers)
        except requests.RequestException as e:
            errmsg = "request %s Failed: %s" % (_url, e)
        if ret.status_code == 200:
            return ret.status_code, json.loads(ret.text)
        else:
            return errmsg

    def handleresults(self, result):

        ret = {}
        nameserver = result['nameServers'][0]
        if 'CLOUDFLARE' in nameserver or 'cloudflare' in nameserver:
            ret['nameServer'] = nameserver
        elif 'AWSDNS' in nameserver or 'awsdns' in nameserver:
            ret['nameServer'] = nameserver
        else:
            ret['nameServer'] = nameserver
        status = result['status']
        if status != 'ACTIVE':
            ret['expires'] = '0000-00-00T00:00:00Z'
        else:
            ret['expires'] = result['expires']

        ret['account'] = self.id
        ret['domain'] = result['domain']
        ret['status'] = result['status']
        ret['createdAt'] = result['createdAt']
        ret['renewAuto'] = result['renewAuto']

        return json.dumps(ret)

    def alldomaininfo(self):

        key = self.key
        secret = self.secret
        url = self.url
        godapihost = self.godapihost


        status, rev = self.goddomain(key, secret, url,godapihost)
        # print rev
        if status == 200:
            for restd in rev:
                # print(restd)
                domain = restd['domain']
                status = restd['status']
                if status == 'ACTIVE':
                    status, subrev = self.goddomaindetail(key, secret, godapihost, url, domain)
                    if status == 200:
                        #print(subrev)
                        print self.handleresults(subrev)
                    else:
                        print "ERROR:"
                else:
                    print "domain is not active : %s => %s" % (domain, status)
        else:
            print "ERROR:"

class Options(object):

    def __init__(self):
        pass

    def parse_command(self):

        #args = self.args

        parser = argparse.ArgumentParser()
        parser.add_argument('-s', '--status', action='store_true', dest='status',
                            help="Get godaddy domain's status")

        parser.add_argument('-d', '--domain', action='store', dest='domain', type=str,
                            help="get godday account domain name")

        parser.add_argument('-t', '--createat', action='store_true', dest='creatat',
                            help='get domain created by time')
        parser.add_argument('-e', action='store_true',dest='expires',
                            help='get domain expires time')
        parser.add_argument('-a', '--renewauto',action='store_true', dest='renewAuto',
                            help='get domain setting auto renew')
        parser.add_argument('-i', '--countid', action='store', dest='countid', type=int,
                            help='Add different values to list')
        parser.add_argument('-H','--host', action='store', dest='host',type=str,
                            help='godaddy host name')

        parser.add_argument('-V','--version', action='version', version=VERSION)
        #args = parser.parse_args()
        return parser