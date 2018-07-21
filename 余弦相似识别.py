# -*- coding: utf-8 -*-
from PIL import Image
import math
import os 
img = Image.open("E:\\work\\Learn_from_blog\\TTyb\\8\\jpg\\2.gif")
his = img.histogram()

#返回的 his 为统计直方图，其类型是一个数组，长度为255，
#his[0] 代表 RGB 颜色 0 的数量有多少，例如该图例如最后一个元素为625，即255（代表的是白色）最多。
#将其统计直方图和 RGB 颜色的值构造成字典，并且按照由高到低排序：
values = {}
for i in range(0,256):
	values[i] = his[i]
#sort方法 key 锁定排序依据
#lambda 根据dict的value进行排序
temp = sorted(values.items(), key= lambda x: x[1], reverse=True)
#由上面print(temp)可已看出颜色255(白色)最多,其次是212 和220
# 获取图片大小，生成一张白底255的图片
img2 = Image.new("P", img.size, 255)
#将统计直方图的颜色依次添加到白底图片中
#获得y坐标, 获得x坐标
for y in range(img.size[1]):
	for x in range(img.size[0]):
		#获得坐标(x,y)的RGB值
		pix = img.getpixel((x,y))
		print(pix)
		#这是要得到的数字
		#if pix == 212:
		#220灰色, 227红色
		if pix ==220 or pix ==227:
			#将黑色0填充到img2中
			img2.putpixel((x,y),0)
#img2.show(1)			

# 纵向切割
# 找到切割的起始和结束的横坐标
inletter = False
foundletter = False
start = 0 
end = 0
#详细注释看readme-8
letters = []

for x in range(img2.size[0]):
	for y in range(img2.size[1]):
		pix = img2.getpixel((x,y))
		if pix != 255:
			inletter = True

	if foundletter ==False and inletter == True:
		foundletter = True
		start = x
		
	if foundletter ==True and inletter ==False:
		foundletter = False
		end = x

		letters.append((start, end))

	inletter = False

class VectorCompare:
	#计算矢量大小
	#计算平方和
	def magnitude(self, concordance):
		total = 0
		# concordance.iteritems:报错'dict' object has no attribute 'iteritems'
		# concordance.items()
		for word, count in concordance.items():
			total += count ** 2
		return math.sqrt(total)

	#计算矢量指尖的cos值
	def relation(self, concordance1, concordance2):
		topvalue = 0
		for word, count in concordance1.items():
			if word in concordance2:
				topvalue += count * concordance2[word]
		return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

#将图片转换为矢量
def buildvector(img):
	d1 = {}
	count = 0

	for i in img.getdata():

		d1[count] = i
		count += 1
	return d1

v = VectorCompare()

iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
		   'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

image_set = []

for letter in iconset:
	for img in os.listdir('E:/work/Learn_from_blog/TTyb/8/iconset/%s/' % (letter)):

		temp = []
		if img:
			temp.append(buildvector(Image.open("E:/work/Learn_from_blog/TTyb/8/iconset/%s/%s" % (letter, img))))

		image_set.append({letter:temp})
#开始破解训练
count = 0

for letter in letters:
	# 切割的起始横坐标, 起始纵坐标, 切割的宽度, 切割的高度
	img3 = img2.crop((letter[0],0,letter[1], img2.size[1]))
	
	guess = []
	#将切割得到的小验证码小片段与每个训练片段进行比较
	for image in image_set:
		# image.iteritems:报错'dict' object has no attribute 'iteritems'
		# 改成image.items()
		for x,y in image.items():
			#print(image.items())
			if len(y) != 0 :
				# y[0]为训练集里面的字母图片，即正确的图片
				# y[0]:{0: 255, 1: 255, 2: 255, 3: 255, 4: 255, 5: 255, 6: 255, 7: 255, 8: 255, 9: 255, 10: 255, 11: 255, 12: 255, 13: 255, 14: 255, 15: 255, 16: 255, 17: 255, 18: 255, 19: 255, 20: 255, 21: 255, 22: 255, 23: 255, 24: 255, 25: 255, 26: 255, 27: 255, 28: 255, 29: 255, 30: 255, 31: 255, 32: 255, 33: 255, 34: 255, 35: 255, 36: 255, 37: 255, 38: 255, 39: 255, 40: 255, 41: 255, 42: 255, 43: 255, 44: 255, 45: 255, 46: 255, 47: 255, 48: 255, 49: 255, 50: 255, 51: 255, 52: 255, 53: 255, 54: 255, 55: 255, 56: 255, 57: 255, 58: 255, 59: 255, 60: 255, 61: 255, 62: 255, 63: 255, 64: 255, 65: 255, 66: 255, 67: 0, 68: 0, 69: 0, 70: 255, 71: 255, 72: 255, 73: 255, 74: 0, 75: 0, 76: 0, 77: 255, 78: 0, 79: 255, 80: 255, 81: 0, 82: 0, 83: 0, 84: 0, 85: 0, 86: 0, 87: 255, 88: 255, 89: 0, 90: 255, 91: 255, 92: 255, 93: 0, 94: 0, 95: 255, 96: 0, 97: 255, 98: 0, 99: 255, 100: 255, 101: 0, 102: 0, 103: 0, 104: 0, 105: 0, 106: 0, 107: 255, 108: 255, 109: 0, 110: 0, 111: 0, 112: 0, 113: 0, 114: 255, 115: 255, 116: 255, 117: 0, 118: 0, 119: 0, 120: 255, 121: 0, 122: 255, 123: 255, 124: 255, 125: 0, 126: 0, 127: 0, 128: 255, 129: 0, 130: 0, 131: 255, 132: 255, 133: 0, 134: 0, 135: 0, 136: 255, 137: 0, 138: 0, 139: 0, 140: 0, 141: 0, 142: 0, 143: 255, 144: 255, 145: 0, 146: 0, 147: 0, 148: 0, 149: 0, 150: 0, 151: 255, 152: 255, 153: 255, 154: 255, 155: 0, 156: 0, 157: 0, 158: 255, 159: 255, 160: 255, 161: 255, 162: 255, 163: 255, 164: 255, 165: 255, 166: 255, 167: 255, 168: 255, 169: 255, 170: 255, 171: 255, 172: 255, 173: 255, 174: 255, 175: 255}
				# buildvector(im3))为切割出来的字母切片，用来和y[0]进行夹角比对
				# buildvector(im3)):{0: 255, 1: 255, 2: 255, 3: 255, 4: 255, 5: 255, 6: 255, 7: 255, 8: 255, 9: 255, 10: 255, 11: 255, 12: 255, 13: 255, 14: 255, 15: 255, 16: 255, 17: 255, 18: 255, 19: 255, 20: 255, 21: 255, 22: 255, 23: 255, 24: 255, 25: 255, 26: 255, 27: 255, 28: 255, 29: 255, 30: 255, 31: 255, 32: 255, 33: 255, 34: 255, 35: 255, 36: 255, 37: 255, 38: 255, 39: 255, 40: 255, 41: 255, 42: 255, 43: 255, 44: 255, 45: 255, 46: 255, 47: 255, 48: 255, 49: 255, 50: 255, 51: 255, 52: 255, 53: 255, 54: 255, 55: 255, 56: 255, 57: 255, 58: 255, 59: 255, 60: 255, 61: 255, 62: 255, 63: 255, 64: 255, 65: 0, 66: 0, 67: 0, 68: 0, 69: 0, 70: 0, 71: 255, 72: 0, 73: 0, 74: 0, 75: 0, 76: 0, 77: 0, 78: 0, 79: 0, 80: 255, 81: 0, 82: 0, 83: 0, 84: 0, 85: 0, 86: 0, 87: 0, 88: 255, 89: 255, 90: 255, 91: 255, 92: 255, 93: 255, 94: 0, 95: 255, 96: 255, 97: 255, 98: 255, 99: 255, 100: 255, 101: 0, 102: 0, 103: 255, 104: 255, 105: 255, 106: 255, 107: 255, 108: 255, 109: 255, 110: 0, 111: 255, 112: 255, 113: 255, 114: 255, 115: 255, 116: 0, 117: 0, 118: 255, 119: 255, 120: 255, 121: 255, 122: 255, 123: 255, 124: 0, 125: 0, 126: 255, 127: 255, 128: 255, 129: 255, 130: 255, 131: 0, 132: 0, 133: 0, 134: 255, 135: 255, 136: 255, 137: 255, 138: 255, 139: 0, 140: 0, 141: 255, 142: 255, 143: 255, 144: 255, 145: 255, 146: 0, 147: 0, 148: 0, 149: 255, 150: 255, 151: 255, 152: 255, 153: 255, 154: 255, 155: 255, 156: 0, 157: 255, 158: 255, 159: 255, 160: 255, 161: 255, 162: 255, 163: 255, 164: 255, 165: 255, 166: 255, 167: 255, 168: 255, 169: 255, 170: 255, 171: 255, 172: 255, 173: 255, 174: 255, 175: 255}
				# x为iconset
				# x依次显示为0，1，2，3，。。。，x,y,z
				guess.append((v.relation(y[0], buildvector(img3)), x))

	# 排序选出夹角最小的（即cos值最大）的向量，夹角越小则越接近重合，匹配越接近
	guess.sort(reverse=True)
	print("", guess[0])

	count += 1