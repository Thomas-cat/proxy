import requests
import telnetlib
from threading import Thread
from bs4 import BeautifulSoup
hide_url = 'http://www.xicidaili.com/wn/'
https_url = 'http://www.xicidaili.com/nn/'
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
	for i in range(1,20):
		th = Thread(target = get_table,args = (hide_url+str(i),))
		ths.append(th)
		th.start()
	for th in ths:
		th.join()
def auto_check():
	global proxies_vaild
	auto_get()
def get_proxies():
	auto_check()
	print (proxies_vaild)
	return proxies_vaild
if __name__ == '__main__':
	get_proxies()


