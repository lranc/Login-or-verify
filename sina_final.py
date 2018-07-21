import requests
import binascii
import re
import json
import rsa
import base64
import time
import logging
from PIL import Image
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

class Weibo():
	def __init__(self):
		self.username = None
		self.password = None
		self.user_uniqueid = None
		self.user_nick = None
		self.session = requests.Session()
		self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"})
		self.session.get("http://weibo.com/login.php")
		return

	def get_su(self,username):
		username_quote = quote_plus(username) #对应手机号和邮箱号
		username_base64 = base64.b64encode(username_quote.encode("utf-8"))  #将其base64编码
		return username_base64.decode("utf-8") #解码
	'''	
	def get_datas_dict(self,su):
		time1 = str(int(time.time()*1000))
		url = "https://login.sina.com.cn/sso/prelogin.php?entry=account&callback=pluginSSOController.preloginCallBack&su="+su+"&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_="+time1
		
		resp= self.session.get(url)
		data = json.loads(re.search(r".*?\((.*)\)", resp.text).group(1).replace("'", '"'))
		return data
	'''
	def get_datas_dict(self,su):
		params = {
		    "entry": "weibo",
		    "callback": "sinaSSOController.preloginCallBack",
		    "rsakt": "mod",
		    "checkpin": "1",
		    "client": "ssologin.js(v1.4.18)",
		    "su": su,
		    "_": int(time.time()*1000),
		}
		try:
		    response = self.session.get("http://login.sina.com.cn/sso/prelogin.php", params=params)
		    #print('111111111111111111')
		    #print(response.text)
		    data = json.loads(re.search(r"\((?P<data>.*)\)", response.text).group("data"))
		except Exception as excep:
		    data = {}
		    logging.error("WeiBoLogin get_datas_dict error: %s", excep)
		logging.debug("WeiBoLogin get_datas_dict: %s", data)
		return data





	def get_sp(self,password, servertime, nonce, pubkey):
		'''
		rsaPublickey = int(pubkey, 16)
		key = rsa.PublicKey(rsaPublickey,  65537)  # 创建公钥
		password = str(servertime) + '\t' + str(nonce) + '\n' + str(password) 
		message = password.encode("utf-8")
		passwd = rsa.encrypt(message, key)
		sp = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
		return sp
		'''
		string = (str(servertime) + "\t" + str(nonce) + "\n" + str(self.password)).encode("utf-8")
		public_key = rsa.PublicKey(int(pubkey, 16), int("10001", 16))
		password = rsa.encrypt(string, public_key)
		sp = binascii.b2a_hex(password)
		return sp.decode()
		
	def login(self,username,password):
		self.username = username
		self.password = password
		self.user_uniqueid = None
		self.user_nick = None
		su = self.get_su(username)
		data = self.get_datas_dict(su)
		if not data:
		    return False
		servertime = data['servertime']
		nonce = data['nonce']
		rsakv = data['rsakv']
		pubkey = data['pubkey']
		pcid = data['pcid']
		sp = self.get_sp(password,servertime,nonce,pubkey)


		postdata = {
			'entry' : 'weibo',
			'geteway' : '1',
			'from' : '',
			'savestate' : '7',
			'useticket': '1',
			'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
			'vsnf': '1',
			'su': su,
			'service': 'miniblog',
			'servertime': servertime,
			'nonce': nonce,
			'pwencode': 'rsa2',
			'rsakv': rsakv,
			'sp': sp,
			'sr': '1366*768',
			'encoding': 'UTF-8',
			'prelt': '529',
			'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
			'returntype': 'META',      

			}

		showpin = data['showpin'] #如果要输入验证码将验证码保存到本地并打开
		if showpin ==1 :
			url = "http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s" % (int(time.time()), data["pcid"])
			
			with open("captcha.jpeg", "wb") as file_out:
				file_out.write(self.session.get(url).content)
			img = Image.open("captcha.jpeg")
			img.show(1)
			code = input("请输入验证码:")
			postdata["pcid"] = data["pcid"]
			postdata['door'] = code
		to_login ="http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=%d" % int(time.time())	
		resp = self.session.post(url=to_login, data=postdata)
		login_loop = resp.content.decode("GBK")
		pa = r'location\.replace\([\'"](.*?)[\'"]\)'
		new_url = re.findall(pa, login_loop)[0]
		z = self.session.get(new_url).text
		print(z)
		#可以添加返回错误的原因, 以及更简洁明了的返回信息
		'''
		if json_data_1["retcode"] == "0":
		    params = {
		        "callback": "sinaSSOController.callbackLoginStatus",
		        "client": "ssologin.js(v1.4.18)",
		        "ticket": json_data_1["ticket"],
		        "ssosavestate": int(time.time()),
		        "_": int(time.time()*1000),
		    }
		    response = self.session.get("https://passport.weibo.com/wbsso/login", params=params)
		    json_data_2 = json.loads(re.search(r"\((?P<result>.*)\)", response.text).group("result"))
		    if json_data_2["result"] is True:
		        self.user_uniqueid = json_data_2["userinfo"]["uniqueid"]
		        self.user_nick = json_data_2["userinfo"]["displayname"]
		        logging.warning("WeiBoLogin succeed: %s", json_data_2)
		    else:
		        logging.warning("WeiBoLogin failed: %s", json_data_2)
		else:
		    logging.warning("WeiBoLogin failed: %s", json_data_1)
		return True if self.user_uniqueid and self.user_nick else False
		'''
if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")
	weibo=Weibo()
	weibo.login("18879206102", "tianyi520")