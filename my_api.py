import urllib.request,re,sqlite3
from datetime import datetime
import multiprocessing as mp

def get_title(article1):
	title = re.findall(r'<h1 class="article-title">(.*?)</h1>',article1,re.S)
	return title

def get_author(article2):
	
	author=re.search(r'<span class="item author">"文/<a href="/news\?uid=(.*?)" target="_blank">(.*?)</a>"</span>',article2,re.S)
	#author=re.findall(r'<span class="item author">文/<a href="/news?" target="_blank">(.*?)</a></span>',article2,re.S)
	return author.group(2)

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
	return content

def get_img(article5):
	img=re.search(r'<img alt="(.*?)" src="(.*?!article\.foil)"',article5,re.M|re.I)
	return img.group(2)

def get_comment(article6):
	comment_count=re.findall(r'<span class="wscn-cm-counter">(.*?)</span>',article6,re.S)
	if comment_count[0]==None:
		return 0
	else:
		return int(comment_count[0])
def spider(pages):
	url='http://wallstreetcn.com/'
	page = urllib.request.urlopen(url)
	pages= page.read().decode('utf-8')
	return pages
	
if __name__ == '__main__':
	try:
		start = datetime.datetime.now()
			#with open('in.txt','w') as f:
				#f.writelines(html)
		start_page = 1
    	end_page = 30


    	# 多进程抓取
    	pages = [i for i in range(start_page, end_page)]
    	p = mp.Pool()
    	p.map_async(spider, pages)
    	p.close()
    	p.join()


		'''conn = sqlite3.connect('test.db')
		conn.execute("INSERT INTO art (title,author,post_at,content,img,comment_count) VALUES (get_title(html),get_author(html),get_time(html),get_content(html),get_img(html),get_comment(html))")
		conn.commit()
		conn.close()'''
		

		print(get_title(html))
		print(get_author(html))
		print(get_time(html))
		print(get_content(html))
		print(get_img(html))
		print(get_comment(html))
	
		#with open('in.txt','w') as f:
			#f.writelines(html)
		end = datetime.datetime.now()
	except Exception as e:
		print(e)