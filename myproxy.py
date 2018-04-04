import requests
import os
import telnetlib
from threading import Thread
from bs4 import BeautifulSoup
https_url = 'http://www.xicidaili.com/wn/'
hide_url = 'http://www.xicidaili.com/wn/'
ua_agent = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
proxies_vaild = []
proxies_vaild_dict ={} 
def check_proxy(proxy):
	global proxies_vaild 
	try:
		telnetlib.Telnet(proxy[1],proxy[2],timeout =1)	
	except:
		pass
	else:
		proxies_vaild.append(proxy)

def check_vaild(proxies):
	ths = []
	for proxy in proxies:
		th = Thread(target = check_proxy,args = (proxy,))
		ths.append(th)
		th.start()
	for th in ths:	
		th.join()

def get_table(url):
	try:
		respon = requests.get(url = url , headers = ua_agent )
		content  = respon.content.decode('utf-8')
		soup = BeautifulSoup(content, 'lxml')
		a = soup.find('table',{'id':'ip_list'})
		b = a.find_all('tr')	
	except:
		return -1
	proxies = []
	for i in range(1,len(b)):
		c = b[i].find_all('td')
		ip = c[1].string
		port = c[2].string 
		ip_type = c[5].string 
		proxies.append((ip_type,ip,port))
	check_vaild(proxies)
def auto_get():
	ths = []
	for i in range(1,40):
		th = Thread(target = get_table,args = (hide_url+str(i),))
		ths.append(th)
		th.start()
	for th in ths:
		th.join()
def write_proxy():
	global proxies_vaild
	i = 0
	for item in proxies_vaild:
		proxies_vaild_dict.update({'%d'%i:item})
		i+=1
	with open('/Users/xiejunjie/py-exam/proxy/my_proxies.txt','w') as f:
		f.write(str(proxies_vaild_dict))
def read_proxy():
	global proxies_uncheck
	if not os.path.exists('/Users/xiejunjie/py-exam/proxy/my_proxies.txt'):
		return -1
	with open('/Users/xiejunjie/py-exam/proxy/my_proxies.txt','r') as f:
		try:
			proxies_uncheck = eval(f.read())
		except:
			return -1 
		if proxies_uncheck == None:
			return -1
		else:
			tmp = []
			for k,v in proxies_uncheck.items():
				tmp.append(v)
			return tmp
def auto_check():
	global proxies_vaild
	ret =  read_proxy()
	if ret == -1:
		auto_get()
	else:
		check_vaild(ret)
		if len(proxies_vaild) < 20:
			auto_get()
def get_proxies():
	auto_check()
	write_proxy()
	return proxies_vaild
if __name__ == '__main__':
	get_proxies()


