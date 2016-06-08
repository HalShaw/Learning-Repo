'''import urllib.request

url='http://wallstreetcn.com/'
data=urllib.request.urlopen(url).read()
data=data.decode('utf-8')
with open ("in.txt",'wb') as f:
	f.writelines(data)'''

'''import re
import urllib.request

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html

def getImg(html):
    reg = r'src="(.+?\.jpg)" pic_ext'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist      
   
html = getHtml("http://tieba.baidu.com/p/2460150866")
print(getImg(html))'''

#coding=utf-8
import urllib.request,re,sqlite3
from datetime import datetime

class Spider(object):
	"""docstring for Spider"""
	def __init__(self):
		self.page=1
		self.url="http://wallstreetcn.com/node/246952"
		
	def get_page(self,cur_page):
		url=self.url
		page = urllib.request.urlopen(url)
		cur_page = page.read().decode('utf-8')
		return cur_page

def save_content(title,author,post_at,content,img,comment_count):
		conn = sqlite3.connect('article.db')
		conn.execute("INSERT INTO art (title,author,post_at,content,img,comment_count)values(?,?,?,?,?,?)",(title,author,post_at,content,img,comment_count))
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
	return str(content[:-4])

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

def spider(url):
	page = urllib.request.urlopen(url)
	pages= page.read().decode('utf-8')
	return pages

def func(page):
    url = "http://wallstreetcn.com/"
    # get参数
    data = {
        "page":page
    }
    full_url=url+'node'+'/'+str(data['page'])
    content = spider(full_url, data)

if __name__ == '__main__':
	try:
		#url = "http://wallstreetcn.com/node/30"
		#html=spider(url)
		start = datetime.now()

		start_page=26
		end_page = 30

		conn = sqlite3.connect('article.db')
		conn.execute("drop table art")
		conn.execute("CREATE TABLE art(title varchar(80) PRIMARY KEY not null, author varchar(10),post_at TEXT not null,content varchar(255) not null,img varchar(20) ,comment_count integer);")
		conn.close() 


		for i in range(start_page, 28):
			url = "http://wallstreetcn.com/"
			full_url=url+'node'+'/'+str(i)
			html=spider('http://wallstreetcn.com/node/247059')

			#save_content(get_title(html),get_author(html),get_time(html),get_content(html),get_img(html),get_comment(html))

			'''print(get_title(html))
			print(get_author(html))
			print(get_time(html))
			print(get_content(html))
			print(get_img(html))
			print(get_comment(html),'\n')'''
		conn = sqlite3.connect('article.db')
		save_content(get_title(html),'get_author(html)',get_time(html),get_content(html),get_img(html),get_comment(html))
		save_content(1,2,3,4,5,6)
		result=conn.execute("SELECT* FROM art")
		#print(list(result))
		conn.close()

		print('title:',get_title(html))
		print('author:',get_author(html))
		print('post_at:',get_time(html))
		print('content:',get_content(html))
		print('img:',get_img(html))
		print('comment_count:',get_comment(html))
	
		with open('in.txt','w') as f:
			f.writelines(html)
	except Exception as e:
		print(e)
		




