#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File Name: godaddydomain.py
Author: windhyz
Mail: windhyz@139.com
Time: 2018-09-20
"""
try:
    import requests, json, time, sys
    from include import *
    from godaddylib import *
except KeyboardInterrupt:
    pass

if __name__ == "__main__":

    #keydict = KEYDICT
    arglist = []
    opts = Options()
    parser = opts.parse_command()
    args = parser.parse_args()
    print(args)
    if args.status:
        arglist.append(args.status)
    if args.domain:
        arglist.append(args.domain)
    if args.creatat:
        arglist.append(args.creatat)
    if args.expires:
        arglist.append(args.expires)
    if args.renewAuto:
        arglist.append(args.renewAuto)
    if args.countid:
        arglist.append(args.countid)
    else:
        print("please input your godaddy acount")
        exit(0)
    if args.host:
        arglist.append(args.host)
    else:
        print("please input godday api domain")

    print(arglist)
    godaddyid = arglist[0]
    host = arglist[1]
    url = URL
    print(arglist)
    print(url)
    if godaddyid in KEYDICT:
        dodaddykey = KEYDICT[godaddyid]
    if godaddyid in SECRETDICT:
        godaddysecret = SECRETDICT[godaddyid]

    gddomain = DodaddyDomain(godaddyid, dodaddykey, godaddysecret, url, host)
    gddomain.alldomaininfo()








