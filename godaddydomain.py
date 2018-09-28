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


    opts = Options()
    parser = opts.parse_command()
    args = parser.parse_args()
    #print(args)
    if args.countid:
        pass
    else:
        print("please input your godaddy acount")
        exit(0)
    if args.host:
        pass
    else:
        print("please input godday api domain")
        exit(0)

    url = URL

    gddomain = DodaddyDomain(args, url)
    if args.domain:
        gddomain.getOneDomaininfo(args.domain)
    else:
        gddomain.alldomaininfo()
