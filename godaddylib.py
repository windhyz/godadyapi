#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File Name: godaddylib.py
Author: windhyz
Mail: windhyz@139.com
Time: 2018-09-20
"""
try:
    import requests, json, argparse, os
    from include import *
except KeyboardInterrupt:
    pass

VERSION = '0.1.0'

class DodaddyDomain(object):

    def __init__(self, args, _url):
        self.args = args
        self.url = _url


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


        if self.args.status:
            ret['status'] = result['status']
        if self.args.domain:
            ret['domain'] = result['domain']
        if self.args.name:
            ret['domain'] = result['domain']
        if self.args.createat:
            ret['createdAt'] = result['createdAt']
        if self.args.expires:
            status = result['status']
            if status != 'ACTIVE':
                ret['expires'] = '0000-00-00T00:00:00Z'
            else:
                ret['expires'] = result['expires']
        if self.args.renewAuto:
            ret['renewAuto'] = result['renewAuto']
        if self.args.nameserver:
            nameserver = result['nameServers'][0]
            if 'CLOUDFLARE' in nameserver or 'cloudflare' in nameserver:
                ret['nameServer'] = nameserver
            elif 'AWSDNS' in nameserver or 'awsdns' in nameserver:
                ret['nameServer'] = nameserver
            else:
                ret['nameServer'] = nameserver

        ret['account'] = self.args.countid

        return json.dumps(ret)

    def outputfile(self,rest):

        filename = self.args.outfile
        try:
            fd = open(filename,'a')
            fd.write(rest + '\n')
        except Exception as e:
            print(e)

        fd.close()

    def alldomaininfo(self):

        #print(self.args)

        acountid = self.args.countid

        if acountid in KEYDICT:
            dodaddykey = KEYDICT[acountid]
        if acountid in SECRETDICT:
            godaddysecret = SECRETDICT[acountid]

        url = self.url

        godapihost = self.args.host

        #print(acountid,dodaddykey,godaddysecret,url,godapihost)

        status, rev = self.goddomain(dodaddykey, godaddysecret, url,godapihost)
        # print rev
        if status == 200:
            for restd in rev:
                # print(restd)
                domain = restd['domain']
                status = restd['status']
                if status == 'ACTIVE':
                    status, subrev = self.goddomaindetail(dodaddykey, godaddysecret, godapihost, url, domain)
                    if status == 200:
                        #print(subrev)
                        if self.args.outfile:
                            self.outputfile(self.handleresults(subrev))
                        else:
                            print self.handleresults(subrev)
                    else:
                        print "ERROR:"
                else:
                    print "domain is not active : %s => %s" % (domain, status)
        else:
            print "ERROR:"

    def getOneDomaininfo(self,udomain):

        acountid = self.args.countid

        if acountid in KEYDICT:
            dodaddykey = KEYDICT[acountid]
        if acountid in SECRETDICT:
            godaddysecret = SECRETDICT[acountid]

        url = self.url

        godapihost = self.args.host
        status, rev = self.goddomain(dodaddykey, godaddysecret, url, godapihost)
        if status == 200:
            for restd in rev:
                #print(restd)
                domain = restd['domain']
                status = restd['status']
                if domain == udomain and status == 'ACTIVE':
                    status, subrev = self.goddomaindetail(dodaddykey, godaddysecret, godapihost, url, udomain)
                    if status == 200:
                        if self.args.outfile:
                            self.outputfile(self.handleresults(subrev))
                        else:
                            print self.handleresults(subrev)
                else:
                    next


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
        parser.add_argument('-n', '--name', action='store_true', dest='name', default=True,
                            help="get godday account domain name")
        parser.add_argument('-t', '--createat', action='store_true', dest='createat',
                            help='get domain created by time')
        parser.add_argument('-e', action='store_true',dest='expires',
                            help='get domain expires time')
        parser.add_argument('-a', '--renewauto',action='store_true', dest='renewAuto',
                            help='get domain setting auto renew')
        parser.add_argument('-i', '--countid', action='store', dest='countid', type=int,
                            help='Add different values to list')
        parser.add_argument('-H','--host', action='store', dest='host',type=str,
                            help='godaddy host name')
        parser.add_argument('-o', '--outfile', action='store', dest='outfile', type=str,
                            help='write info output to file')
        parser.add_argument('-N', '--nameserver', action='store_true', dest='nameserver',
                            help="domain's  name server")
        parser.add_argument('-V','--version', action='version', version=VERSION)
        #args = parser.parse_args()
        return parser