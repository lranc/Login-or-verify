# -*- coding: utf-8 -*-
import time
import io
import random
from selenium import webdriver
#调用控制鼠标的库
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from PIL import ImageChops
import math


def open_browser(url):
	global browser
	browser = webdriver.Chrome()
	browser.set_page_load_timeout(90)

	try:
		browser.get(url)
		if "400 Bad request" in browser.page_source:
			browser.get(url)

	except:
		#超过90秒强制停止加载
		browser.execute_script('window.stop()')
		if "400 Bad request" in browser.page_source:
			browser.get(url)
		else:
			pass
	time.sleep(5)

def input_keyword(keyword):
	browser.find_element_by_id("keyword").clear()
	browser.find_element_by_id("keyword").send_keys(keyword)
	time.sleep(3)
	browser.find_element_by_id("btn_query").click()
	time.sleep(3)

def click_image():
	browser.find_element_by_class_name("gt_slider_knob").click()
	time.sleep(3)



def get_screen_image():
	try:
		#定位到验证码的框
		captcha_element = browser.find_element_by_class_name("gt_box")
	except:
		input_keyword(keyword)
		captcha_element = browser.find_element_by_class_name("gt_box")
	#获得验证码区域的坐标属性以及大小
	locations = captcha_element.location
	sizes = captcha_element.size

	left = int(locations["x"])
	top = int(locations["y"])
	right = left + int(sizes["width"])
	bottom = top + int(sizes["height"])

	#截图
	screenshot = browser.get_screenshot_as_png()
	screenshot = Image.open(io.BytesIO(screenshot))
	png = screenshot.crop((left,top,right,bottom))
	#png.save(str(int(time.time()))+".png")

	time.sleep(1)
	return png

#获取滑块的图片是为了得到滑块的宽度, 以排除示例图片的干扰
def getWidth():
	#找到滑块并滑动
	slider = browser.find_element_by_class_name("gt_slice")
	sizes = slider.size
	width = sizes["width"]
	return width

#获得滑动偏移量
def get_offset():
	img1 = get_screen_image()
	click_image()
	#拖动鼠标后,观察出现的验证码与原图区域的区别
	img2 = get_screen_image()
	img3 = ImageChops.difference(img1,img2)
	#img3.show(1)
	#img3.save(str(int(time.time())) + ".png")
	w1, h1 = img1.size
	w2, h2 = img2.size
	w3, h3 = img3.size
	#如果图片尺寸不一致,则错误
	if w1 != w2 or h1 != h2:
		return False

	slider = getWidth()
	print('开始循环',w3,h3)
	for x in range(slider,w3):
		#print(x)
		for y in range(0,h3):
			pix1 = img1.getpixel((x,y))
			pix2 = img2.getpixel((x,y))
			pix3 = img3.getpixel((x,y))
			#print(pix1)
			#print(pix1[0],pix2[1],pix3[2])
			#RGB 某个值大于70 就色彩鲜艳
			#判断色彩鲜艳与否
			if pix3[0] > 70 or pix3[1] > 70 or pix3[2] > 70 and abs(pix1[0] - pix2[0]) < 60 and abs(
                            pix1[1] - pix2[1]) < 60 and abs(pix1[2] - pix2[2]) < 60 :
				#滑块坐标有5个位移是空白的
				return x-5
	#如果没有找到正确的偏移量返回一个假的偏移值, 防止程序中断
	return 55

#拖放滑块
def drag_and_drop(x_offset, y_offset):
	#找到滑块并拖动
	source = browser.find_element_by_class_name("gt_slider_knob")
	#调用鼠标操作并拖动,perform() 提交操作
	#ActionChains(browser).drag_and_drop_by_offset(source, x_offset, y_offset).perform()
	ActionChains(browser).click_and_hold(source).move_by_offset(0, y_offset).perform()
	time.sleep(0.05)
	c = 0.3	
	lis = []
	x =x_offset
	while x > 10:
		q = random.uniform(-4,20)
		lis.append(q)
		x = x-q
	lis.append(x-0.5)
	lis.sort(reverse=True)
	lis.append(-0.2)
	lis.append(-0.1)
	print(lis)
	
	
	for i in lis:					
		ActionChains(browser).move_by_offset(i,0).perform()
		s=random.uniform(0.01,0.03)
		c += s/2
		time.sleep(c)													
	ActionChains(browser).move_by_offset(0.1,0).release().perform()	
		

	time.sleep(3)

def main(url,keyword):
	open_browser(url)
	input_keyword(keyword)
	offset = get_offset()
	print(offset)
	drag_and_drop(x_offset=offset, y_offset=0)


if __name__ == '__main__':
	url = 'http://www.gsxt.gov.cn/corp-query-homepage.html'
	keyword = "中国联通"
	main(url,keyword)