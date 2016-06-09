# -*-coding:utf-8-*-

import urllib.request
import re
import sqlite3
import time
import random
import threading
import multiprocessing
import urllib.error
import sys
from datetime import datetime

class Article(object):
	def __init__(self):
		self.url="http://wallstreetcn.com/"

	def get_content(self,article):
		#使用正则表达式匹配出标题、作者、日期、内容、第一张大图的url、评论数
		title = re.findall(r'<h1 class="article-title">(.*?)</h1>',article,re.S)
		author=re.search(r'<span class="item author">(.*?)target="_blank">(.*?)</a>(.*?)</span>',article,re.S)
		post_at=re.findall(r'<span class="item time">(.*?)</span>',article,re.S)
		time=post_at[0]
		year=time[:4]
		month=time[5:7]
		day=time[8:10]
		hour=time[12:]#对有中文时间格式处理，返回值为datetime格式
		content=re.findall(r'<p>(.*?)</p>',article,re.S)
		img=re.search(r'<img alt="(.*?)" src="(.*?!article\.foil)"',article,re.M|re.I)
		comment_count=re.findall(r'<span class="wscn-cm-counter">(.*?)</span>',article,re.S)

		if img==None and comment_count[0]==None:#有可能文章没有图片和评论，考虑以下几种情况
			return str(title[0]),str(author.group(2)),datetime.strptime(year+'-'+month+'-'+day+' '+hour,'%Y-%m-%d %H:%M:%S'),''.join(content[:-4]),None,0
		elif img!=None and comment_count[0]==None:
			return str(title[0]),str(author.group(2)),datetime.strptime(year+'-'+month+'-'+day+' '+hour,'%Y-%m-%d %H:%M:%S'),''.join(content[:-4]),str(img.group(2)),0
		elif img==None and comment_count[0]!=None:
			return str(title[0]),str(author.group(2)),datetime.strptime(year+'-'+month+'-'+day+' '+hour,'%Y-%m-%d %H:%M:%S'),''.join(content[:-4]),None,int(comment_count[0])
		else:
			return str(title[0]),str(author.group(2)),datetime.strptime(year+'-'+month+'-'+day+' '+hour,'%Y-%m-%d %H:%M:%S'),''.join(content[:-4]),str(img.group(2)),int(comment_count[0])

	def save_content(self,title,author,post_at,content,img,comment_count):
		#连接并保存到数据库
		conn = sqlite3.connect('article.db')
		conn.execute("drop table art")#如果存在一个art表，删除，新建一个art表
		conn.execute("CREATE TABLE art(title varchar(80) PRIMARY KEY not null, author varchar(10),post_at TEXT not null,content varchar(255) not null,img varchar(20) ,comment_count integer);")
		conn.execute("INSERT INTO art (title,author,post_at,content,img,comment_count)values(?,?,?,?,?,?)",(title,author,post_at,content,img,comment_count))
		result=conn.execute("SELECT* FROM art")
		return list(result)
		conn.close()

	def spider(self):
		cou=1
		#for i in range(1999,20002):#顺序生成URL
		for i in random.sample(range(1999,20016),500):#随机生成url
			try:
				full_url=self.url+'node'+'/'+str(i)#URL格式
				page = urllib.request.urlopen(full_url,timeout=10)#设置请求时间限制
				pages= page.read().decode('utf-8','ignore')
				lst=self.get_content(pages)
				#self.save_content(lst[0],lst[1],lst[2],lst[3],lst[4],lst[5])#不打印出结果
				print(self.save_content(lst[0],lst[1],lst[2],lst[3],lst[4],lst[5]))#打印出结果
				print('Successfully Downloaded...\n')
				cou+=1
				time.sleep(2)
				if cou>300:
					sys.exit()
				else:
					continue
			except urllib.error.URLError as e:
				print(e)
				
				
	def main(self):
		#多线程和多进程爬取
		#my_thread = threading.Thread(target = self.spider)#多线程
		my_thread = multiprocessing.Process(target = self.spider)#多进程
		my_thread.start()
		my_thread.join()

if __name__ == '__main__':
	a=Article()#实例化
	a.main()






