import requests
from threading import Thread
import time
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from myproxy import get_proxies
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
reg = re.compile(r'var url = "(.*?)"',re.S)
url = 'https://ccckk8.com/fanhao/detail/22147#header'
url_profile = 'https://ccckk8.com/user/profile'
url_check = input('请输入ccckk8分享网址:\n')
ua_agent = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
proxies  = get_proxies()
req = requests.Session()

def run(proxy): 
	try:
		ret = req.get(url = url_check, headers = ua_agent,verify = False,proxies = proxy,timeout = 2)

	except:
		pass
def main():
	ths = []
	for item in proxies:
		proxy = {item[0].lower():item[0].lower()+'://'+item[1]+':'+item[2]}
		th = Thread(target = run,args = (proxy,))	
		ths.append(th)
		th.start()
	for item in ths:
		item.join()


main()
