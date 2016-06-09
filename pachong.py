# -*-coding:utf-8-*-

import urllib.request
import re
import sqlite3
import time
import random
import threading
import multiprocessing
import urllib.error
import socket
from datetime import datetime

class Spider(object):
	def __init__(self):
		self.url="http://wallstreetcn.com/"
	def get_content(self,article):
		title = re.findall(r'<h1 class="article-title">(.*?)</h1>',article,re.S)
		author=re.search(r'<span class="item author">(.*?)target="_blank">(.*?)</a>(.*?)</span>',article,re.S)
		post_at=re.findall(r'<span class="item time">(.*?)</span>',article,re.S)
		time=post_at[0]
		year=time[:4]
		month=time[5:7]
		day=time[8:10]
		hour=time[12:]
		content=re.findall(r'<p>(.*?)</p>',article,re.S)
		img=re.search(r'<img alt="(.*?)" src="(.*?!article\.foil)"',article,re.M|re.I)
		comment_count=re.findall(r'<span class="wscn-cm-counter">(.*?)</span>',article,re.S)
		if img==None and comment_count[0]==None:
			return str(title[0]),str(author.group(2)),datetime.strptime(year+'-'+month+'-'+day+' '+hour,'%Y-%m-%d %H:%M:%S'),''.join(content[:-4]),None,0
		elif img!=None and comment_count[0]==None:
			return str(title[0]),str(author.group(2)),datetime.strptime(year+'-'+month+'-'+day+' '+hour,'%Y-%m-%d %H:%M:%S'),''.join(content[:-4]),str(img.group(2)),0
		elif img==None and comment_count[0]!=None:
			return str(title[0]),str(author.group(2)),datetime.strptime(year+'-'+month+'-'+day+' '+hour,'%Y-%m-%d %H:%M:%S'),''.join(content[:-4]),None,int(comment_count[0])
		else:
			return str(title[0]),str(author.group(2)),datetime.strptime(year+'-'+month+'-'+day+' '+hour,'%Y-%m-%d %H:%M:%S'),''.join(content[:-4]),str(img.group(2)),int(comment_count[0])

	def save_content(self,title,author,post_at,content,img,comment_count):
		conn = sqlite3.connect('article.db')
		conn.execute("INSERT INTO art (title,author,post_at,content,img,comment_count)values(?,?,?,?,?,?)",(title,author,post_at,content,img,comment_count))
		result=conn.execute("SELECT* FROM art")
		cur = conn.cursor()
		count=cur.fetchall()
		#c=count[0]
		print(count)
		return list(result)
		conn.close()

	def spider(self):
		for i in range(1999,2015):
			try:
				timeout = 20
				socket.setdefaulttimeout(timeout)
				#url = "http://wallstreetcn.com/"
				full_url=self.url+'node'+'/'+str(i)
				page = urllib.request.urlopen(full_url)
				pages= page.read().decode('utf-8','ignore')
				lst=self.get_content(pages)
				self.save_content(lst[0],lst[1],lst[2],lst[3],lst[4],lst[5])
				#print(save_content(get_title(pages),get_author(pages),get_time(pages),get_content(pages),get_img(pages),get_comment(pages)))
				print('Successfully Downloaded...\n')
				time.sleep(1)
				#return get_title(pages),get_author(pages),get_time(pages),get_content(pages),get_img(pages),get_comment(pages)
			except urllib.error.URLError as e:
				print(e)
				continue


	def main(self):
		my_thread = threading.Thread(target = self.spider)
		#my_thread = multiprocessing.Process(target = spider)
		my_thread.start()
		my_thread.join()

'''
def get_content(article):
		title = re.findall(r'<h1 class="article-title">(.*?)</h1>',article,re.S)
		author=re.search(r'<span class="item author">(.*?)target="_blank">(.*?)</a>(.*?)</span>',article,re.S)
		post_at=re.findall(r'<span class="item time">(.*?)</span>',article,re.S)
		time=post_at[0]
		year=time[:4]
		month=time[5:7]
		day=time[8:10]
		hour=time[12:]
		content=re.findall(r'<p>(.*?)</p>',article,re.S)
		img=re.search(r'<img alt="(.*?)" src="(.*?!article\.foil)"',article,re.M|re.I)
		comment_count=re.findall(r'<span class="wscn-cm-counter">(.*?)</span>',article,re.S)
		if img==None and comment_count[0]==None:
			return str(title[0]),str(author.group(2)),datetime.strptime(year+'-'+month+'-'+day+' '+hour,'%Y-%m-%d %H:%M:%S'),''.join(content[:-4]),None,0
		elif img!=None and comment_count[0]==None:
			return str(title[0]),str(author.group(2)),datetime.strptime(year+'-'+month+'-'+day+' '+hour,'%Y-%m-%d %H:%M:%S'),''.join(content[:-4]),str(img.group(2)),0
		elif img==None and comment_count[0]!=None:
			return str(title[0]),str(author.group(2)),datetime.strptime(year+'-'+month+'-'+day+' '+hour,'%Y-%m-%d %H:%M:%S'),''.join(content[:-4]),None,int(comment_count[0])
		else:
			return str(title[0]),str(author.group(2)),datetime.strptime(year+'-'+month+'-'+day+' '+hour,'%Y-%m-%d %H:%M:%S'),''.join(content[:-4]),str(img.group(2)),int(comment_count[0])
def save_content(title,author,post_at,content,img,comment_count):
		conn = sqlite3.connect('article.db')
		conn.execute("INSERT INTO art (title,author,post_at,content,img,comment_count)values(?,?,?,?,?,?)",(title,author,post_at,content,img,comment_count))
		result=conn.execute("SELECT count(*) FROM art")
		cur = conn.cursor()
		count=cur.fetchall()
		#c=count[0]
		print(list(result))
		#return list(result)
		conn.close()

def get_title(article1):
	title = re.findall(r'<h1 class="article-title">(.*?)</h1>',article1,re.S)
	return str(title[0])

def get_author(article2):
	author=re.search(r'<span class="item author">(.*?)target="_blank">(.*?)</a>(.*?)</span>',article2,re.S)
	return str(author.group(2))

def get_time(article3):
	post_at=re.findall(r'<span class="item time">(.*?)</span>',article3,re.S)
	time=post_at[0]
	year=time[:4]
	month=time[5:7]
	day=time[8:10]
	hour=time[12:]
	return datetime.strptime(year+'-'+month+'-'+day+' '+hour,'%Y-%m-%d %H:%M:%S')

def get_content(article4):
	content=re.findall(r'<p>(.*?)</p>',article4,re.S)
	return ''.join(content[:-4])

def get_img(article5):
	img=re.search(r'<img alt="(.*?)" src="(.*?!article\.foil)"',article5,re.M|re.I)
	if img==None:
		return None
	else:
		return str(img.group(2))

def get_comment(article6):
	comment_count=re.findall(r'<span class="wscn-cm-counter">(.*?)</span>',article6,re.S)
	if comment_count[0]==None:
		return 0
	else:
		return int(comment_count[0])

def spider():
	for i in range(1999,2015):
		try:
			timeout = 20
			socket.setdefaulttimeout(timeout)
			url = "http://wallstreetcn.com/"
			full_url=url+'node'+'/'+str(i)
			page = urllib.request.urlopen(full_url)
			pages= page.read().decode('utf-8','ignore')
			lst=get_content(pages)
			save_content(lst[0],lst[1],lst[2],lst[3],lst[4],lst[5])
			#print(save_content(get_title(pages),get_author(pages),get_time(pages),get_content(pages),get_img(pages),get_comment(pages)))
			print('Successfully Downloaded...\n')
			time.sleep(1)
			#return get_title(pages),get_author(pages),get_time(pages),get_content(pages),get_img(pages),get_comment(pages)
		except urllib.error.URLError as e:
			print(e)
			continue

def main():
	#my_thread = threading.Thread(target = spider)
	my_thread = multiprocessing.Process(target = spider)
	my_thread.start()
	my_thread.join()
	'''			

if __name__ == '__main__':
	a=Spider()

	a.main()






