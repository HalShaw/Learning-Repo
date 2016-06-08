import urllib.request,re,sqlite3
from datetime import datetime
import multiprocessing as mp
import threading,time

class Article(object):
	"""docstring for save_content"""
	def __init__(self, title,author,post_at,content,img,comment_count):
		self.title = title
		self.author=author
		self.post_at=post_at
		self.content=content
		self.img=img
		self.comment_count=comment_count
	def create_db(self):
		conn = sqlite3.connect('article.db')
		conn.execute('''CREATE TABLE art(title varchar(80) PRIMARY KEY not null, author varchar(10),post_at text not null,content varchar(1000) not null,img varchar(20) ,comment_count int);''')
		conn.close() 
def save_content(title,author,post_at,content,img,comment_count):
		conn = sqlite3.connect('article.db')
		conn.execute("INSERT INTO art(title,author,post_at,content,img,comment_count)values(?,?,?,?,?,?)",(title,author,post_at,content,img,comment_count))
		conn.close() 
def check(result):
	conn = sqlite3.connect('article.db')
	result=conn.execute("SELECT* FROM art")
	print(result)

def get_title(article1):
	title = re.findall(r'<h1 class="article-title">(.*?)</h1>',article1,re.S)
	return str(title[0])

def get_author(article2):
	
	author=re.findall(r'<span class="item author">"文/<a href="/news\?uid=(.*?)" target="_blank">(.*?)</a>"</span>',article2,re.S)
	#author=re.findall(r'<span class="item author">文/<a href="/news?" target="_blank">(.*?)</a></span>',article2,re.S)
	return author

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
		conn.execute("CREATE TABLE art(title varchar(80) PRIMARY KEY not null, author varchar(10),post_at TEXT not null,content varchar(1000) not null,img varchar(20) ,comment_count int);")
		conn.close() 


		for i in range(start_page, end_page):
			url = "http://wallstreetcn.com/"
			full_url=url+'node'+'/'+str(i)
			html=spider(full_url)

			save_content(get_title(html),get_author(html),get_time(html),get_content(html),get_img(html),get_comment(html))

			'''print(get_title(html))
			print(get_author(html))
			print(get_time(html))
			print(get_content(html))
			print(get_img(html))
			print(get_comment(html),'\n')'''
		conn = sqlite3.connect('article.db')
		result=conn.execute("SELECT* FROM art")
		print(result)
		conn.close()

		'''url = "http://wallstreetcn.com/"
		# 多进程抓取
		for i in range(start_page, end_page):
			full_url=url+'node'+'/'+str(i)
			t=map_async(spider)
			t.start()
			t.join()
			time.sleep(2)

			p = mp.Pool()
			content=p.map_async(spider,full_url)
			print(content)
			p.close()
			p.join()'''


		'''conn = sqlite3.connect('test.db')
		conn.execute("INSERT INTO art (title,author,post_at,content,img,comment_count) VALUES (get_title(html),get_author(html),get_time(html),get_content(html),get_img(html),get_comment(html))")
		conn.commit()
		conn.close()'''
		

		
	
		#with open('in.txt','w') as f:
			#f.writelines(html)
		end = datetime.now()
		print(end-start)
	except Exception as e:
		print(e)

