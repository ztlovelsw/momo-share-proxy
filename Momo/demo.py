

例1：Python http/sock5:
############## 例1--开始 ##############
#coding=utf-8
import requests

#请求地址
targetUrl = "http://baidu.com"

#代理服务器
proxyHost = "ip"
proxyPort = "port"

proxyMeta = "http://%(host)s:%(port)s" % {
    "host" : proxyHost,
    "port" : proxyPort,
}

#pip install -U requests[socks]  socks5代理
# proxyMeta = "socks5://%(host)s:%(port)s" % {
#     "host" : proxyHost,
#     "port" : proxyPort,
# }

proxies = {
    "http"  : proxyMeta,
}

resp = requests.get(targetUrl, proxies=proxies)
print resp.status_code
print resp.text
############## 例1--结束 ##############

例2：账号密码：http方式
############## 例2--开始 ##############
#coding=utf-8
import requests

#请求地址
targetUrl = "http://httpbin.org/ip"

proxies = {
    'http': 'http://user:pwd@121.239.87.32:44101',
}

resp = requests.get(targetUrl, proxies=proxies,  verify=False)
print (resp.status_code)
print (resp.text)
############## 例2--结束 ##############


例3：账号密码：SoCKS5方式
############## 例3--开始 ##############
from urllib3.contrib.socks import SOCKSProxyManager

#coding=utf-8
import requests
import socket
import socks

#请求地址
test_url = "http://httpbin.org/ip"

socks.set_default_proxy(socks.SOCKS5, "117.26.193.90", 54104,'user','pwd')
socket.socket = socks.socksocket
resp = requests.get(test_url).text
print(resp)
############## 例3--结束 ##############

例4: 访问https
############## 例4--开始 ##############
#coding=utf-8
import requests
#请求地址
targetUrl = "https://httpbin.org/ip"

proxies = {
    'https': 'http://ydmye:770393@115.239.211.247:2018',
}

resp = requests.get(targetUrl, proxies=proxies,  verify=False)
print (resp.status_code)
print (resp.text)
############## 例4--结束 ##############
