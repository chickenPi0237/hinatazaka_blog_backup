import urllib.request as req
import urllib.parse
import bs4
import csv
import time
import os
from os import listdir
from os.path import isfile, join
import re
src = 'https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct='
hinatazakaWeb = 'https://www.hinatazaka46.com'
memberFolderPath = 'D:\Anaconda3\hinatazakaBlogCrawler\\'

#old ua 2023/10/15
#ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KTML, like Gecko) Chrome/74.0.3729.172 Sarfari/537.36 Vivaldi/2.5.1525.48'
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'

def storeArticle(artName_fun,artDate_fun,artTitle_fun,articleText_fun,sameArtIndex,htmlData,articleHref):
	samePath = '-'+str(sameArtIndex)
	#寫入成txt可能因為不同成員的blog格式不同導致無換行等問題
	if sameArtIndex==None:
		with open(memberFolderPath+artName_fun+'\\'+artDate_fun+'\\'+artDate_fun+'.txt','a',encoding='utf-8') as outfile:
				outfile.write(artTitle_fun)
				outfile.write('\n')
				outfile.write(artName_fun)
				outfile.write('\n')
				outfile.write(artDate_fun)
				for line in articleText_fun:
					outfile.write(line.text)
		#儲存html
		with open(memberFolderPath+artName_fun+'\\'+artDate_fun+'\\'+artDate_fun+'.html','a',encoding='utf-8') as outfile:
				outfile.write(htmlData)
		#儲存網址
		with open(memberFolderPath+artName_fun+'\\'+artDate_fun+'\\artcleHref.txt','a',encoding='utf-8') as outfile:
				outfile.write(articleHref)
	else:
		with open(memberFolderPath+artName_fun+'\\'+artDate_fun+samePath+'\\'+artDate_fun+samePath+'.txt','a',encoding='utf-8') as outfile:
				outfile.write(artTitle_fun)
				outfile.write('\n')
				outfile.write(artName_fun)
				outfile.write('\n')
				outfile.write(artDate_fun)
				for line in articleText_fun:
					outfile.write(line.text)
		with open(memberFolderPath+artName_fun+'\\'+artDate_fun+samePath+'\\'+artDate_fun+samePath+'.html','a',encoding='utf-8') as outfile:
				outfile.write(htmlData)
		with open(memberFolderPath+artName_fun+'\\'+artDate_fun+samePath+'\\artcleHref.txt','a',encoding='utf-8') as outfile:
				outfile.write(articleHref)
	
def storeArtImg(articleImgs_fun,artName_fun,artDate_fun,sameArtIndex):
	samePath = '-'+str(sameArtIndex)
	if sameArtIndex == None:
		#抓取圖片
		for articleImg in articleImgs_fun:
			#in case articleImg no 'src'
			try :
				print('Not In Same Time article:',articleImg['src'])
				if re.search('cdn\.hinatazaka46\.com/.*',articleImg['src']) != None:
					try:
						req.urlretrieve(articleImg['src'],memberFolderPath+artName_fun+'\\'+artDate_fun+'\\'+artDate_fun+'-'+articleImg['src'].split('/')[-1])
						#windows cmd copy file時如路徑有空白需用""包住 格式: copy "FILE" WHERE
						command = 'copy \"'+memberFolderPath+artName_fun+'\\'+artDate_fun+'\\'+artDate_fun+'-'+articleImg['src'].split('/')[-1]+'\" '+memberFolderPath+artName_fun+'\\'+'pictures'+'\\' 
						#print(command)
						os.popen(command)
					except Exception as e:
						print('error is:',e)
						print('error img url is:',articleImg['src'])
				else:
					print('Not In Same Time article:插圖 or Logo')
			except :
				print('no src?', articleImg)
			
	else:
		for articleImg in articleImgs_fun:
			print('In Same Time article:',articleImg['src'])
			if re.search('cdn\.hinatazaka46\.com/.*',articleImg['src']) != None:
				try:
					req.urlretrieve(articleImg['src'],memberFolderPath+artName_fun+'\\'+artDate_fun+samePath+'\\'+artDate_fun+samePath+'-'+articleImg['src'].split('/')[-1])
					#windows cmd copy file時如路徑有空白需用""包住 格式: copy "FILE" WHERE
					command = 'copy \"'+memberFolderPath+artName_fun+'\\'+artDate_fun+samePath+'\\'+artDate_fun+samePath+'-'+articleImg['src'].split('/')[-1]+'\" '+memberFolderPath+artName_fun+'\\'+'pictures'+'\\' 
					os.popen(command)
				except Exception as e:
					print('error is:',e)
					print('error img url is:',articleImg['src'])
			else:
				print('In Same Time article:插圖 or Logo')



def crawlArticle(articlesSrc_arg,newBlogList):
	i=0
	sameTimeArtNum = 0

	'''for artSrcFun in articlesSrc_arg:
		print('in fun src:'+artSrcFun['href'])'''

	for articleSrc in articlesSrc_arg:
		print(articleSrc['href']) #ex:/s/official/diary/detail/30040?ima=0000&cd=member
		
		request = req.Request(hinatazakaWeb+articleSrc['href'])
		request.add_header('User-Agent', ua)
		try:
			with req.urlopen(request, timeout=3) as response:
				data = response.read().decode('utf-8')
		except urllib.error.URLError:
			print('smth wrong, timed out') 
		articleRoot = bs4.BeautifulSoup(data,'html.parser')
		articleTitle = articleRoot.select('div.c-blog-article__title')
		articleDate = articleRoot.select('div.c-blog-article__date')
		articleName = articleRoot.select('div.c-blog-article__name')
		articleText = articleRoot.select('div.c-blog-article__text')
		articleImgs = articleRoot.select('div.c-blog-article__text img')
		#print('haha',articleImgs)


		i+=1
		print(i)
		print(articleTitle[0].text)
		print(articleDate[0].text)
		print(articleName[0].text)
		#姓名與日期字串美化
		artName = articleName[0].text.replace('\n','')
		artName = artName.replace(' ','')
		artDate = articleDate[0].text.replace('\n','')
		artDate = artDate.replace(':','-')
		artTitle = articleTitle[0].text.replace('\n','')

		#成員資料夾
		if not os.path.exists(memberFolderPath+artName):
			os.makedirs(memberFolderPath+artName)
		#圖片集中資料夾
		if not os.path.exists(memberFolderPath+artName+'\\'+'pictures'):
			os.makedirs(memberFolderPath+artName+'\\'+'pictures')
		#依照日期分資料夾
		if not os.path.exists(memberFolderPath+artName+'\\'+artDate):
			os.makedirs(memberFolderPath+artName+'\\'+artDate)
			sameTimeArtNum = 0
			storeArticle(artName,artDate,artTitle,articleText,None,data,articleSrc['href'])
			storeArtImg(articleImgs,artName,artDate,None)
			newBlogList.append(artName)
		else:
			with open(memberFolderPath+artName+'\\'+artDate+'\\artcleHref.txt','r',encoding='utf-8') as checkfile:
				artHref = checkfile.readline()
				print('compare:')
				print(artHref)
				print(articleSrc['href'])
				if articleSrc['href'] == artHref:
					return 1
				else:
					sameTimeArtNum += 1
					samePath = '-'+str(sameTimeArtNum)
					os.makedirs(memberFolderPath+artName+'\\'+artDate+samePath)
					storeArticle(artName,artDate,artTitle,articleText,sameTimeArtNum,data,articleSrc['href'])
					storeArtImg(articleImgs,artName,artDate,sameTimeArtNum)
					newBlogList.append(artName)
		

		'''#儲存原始網頁
		with open(memberFolderPath+artName+'\\'+artDate+'\\'+artDate+'.html','a',encoding='utf-8') as outfile:
				outfile.write(data)'''

		'''#寫入成txt可能因為不同成員的blog格式不同導致無換行等問題
		with open(memberFolderPath+artName+'\\'+artDate+'\\'+artDate+'.txt','a',encoding='utf-8') as outfile:
				outfile.write(artTitle)
				outfile.write('\n')
				outfile.write(artName)
				outfile.write('\n')
				outfile.write(artDate)
				for line in articleText:
					outfile.write(line.text)'''
		'''#抓取圖片
		for articleImg in articleImgs:
			print(articleImg['src'])
			if re.search('\.jpg',articleImg['src']) != None:
				try:
					req.urlretrieve(articleImg['src'],memberFolderPath+artName+'\\'+artDate+'\\'+artDate+'-'+articleImg['src'].split('/')[-1])
					#windows cmd copy file時如路徑有空白需用""包住 格式: copy "FILE" WHERE
					command = 'copy \"'+memberFolderPath+artName+'\\'+artDate+'\\'+artDate+'-'+articleImg['src'].split('/')[-1]+'\" '+memberFolderPath+artName+'\\'+'pictures'+'\\' 
					os.popen(command)
				except Exception as e:
					print('error is:',e)
					print('error img url is:',articleImg['src'])
			else:
				print('插圖 or Logo')
			#with open(artDate+str(j)+'.png','wb') as outImg:
			#	outImg.write(imgHtml)'''
		time.sleep(1)
	return 0



'''a = r"https://cdn.hinatazaka46.com/images/14/243/ff27912db4ed66b65b619cbf1674d-05.png"
b = r"https://twemoji.maxcdn.com/v/12.1.5/72x72/1f306.png"
c = r"https://cdn.hinatazaka46.com/images/14/243/ff27912db4ed66b65b619cbf1674d-04.jpg"
#print(re.search('cdn\.hinatazaka46\.com/images/.*\.jpg|cdn\.hinatazaka46\.com/images/.*\.png',c))
print(re.search('cdn\.hinatazaka46\.com/.*',c))'''
startTime = time.time()

fatchBlogFlag = True
isDupicated = 0 #1 yes, 0 no
memberIndex = 0#0 poka 1 井口 3 柿崎芽實
memberList = ['ポカ', '井口真緒', '潮紗理菜', '柿崎芽實', '影山優佳',
				'加藤史帆', '齊藤京子', '佐々木久美', '佐々木美玲', '高瀬愛奈',
				'高本彩花', '東村芽依', '金村美玖', '河田陽菜', '小坂菜緒', 
				'富田鈴花', '丹生明里', '濱岸ひより', '松田好花', '宮田愛萌', 
				'渡邊美穗', '上村ひなの', '高橋未來虹', '森本茉莉', '山口陽世', 
				'石塚瑶季', '岸帆夏', '小西夏菜実', '清水理央', '正源司陽子', 
				'竹内希来里', '平岡海月', '藤嶌果歩', '宮地すみれ', '山下葉留花', 
				'渡辺莉奈',
			]
graduatedList = [0,1,1,1,1,
				0,0,0,0,0,
				0,0,0,0,0,
				0,0,0,0,1,
				1,0,0,0,0,
				0,1,0,0,0,
				0,0,0,0,0,
				0
				]
newBlogList = []

while(1):
	pageIndex = 0
	if memberIndex == len(memberList):
		print('all finished')
		break
	if graduatedList[memberIndex]==1:
		print(memberList[memberIndex]+' 已畢業')
		fatchBlogFlag = False
	'''
	#因為memi畢業 原五十音順為第三位即是Kakizaki Memi
	if memberIndex == 3:
		print('柿崎芽實 已畢業')
		fatchBlogFlag = False
	#因為井口畢業 原五十音順為第一位即是Iguchi Mao
	if memberIndex == 1:
		print('井口真緒 已畢業')
		fatchBlogFlag = False
	if memberIndex == 20:
		print('渡邊美穗 已畢業')
		fatchBlogFlag = False
	if memberIndex == 19:
		print('宮田愛萌 已畢業')
		fatchBlogFlag = False
	if memberIndex == 4:
		print('影山優佳 已畢業')
		fatchBlogFlag = False
	if memberIndex == 2:
		print('潮紗理菜 已畢業')
		fatchBlogFlag = False
	if memberIndex == 26:
		print('岸帆夏 已畢業')
		fatchBlogFlag = False'''
	if memberIndex == 0:
		#poka 專屬判斷
		request = req.Request(src+'000'+'&page='+str(pageIndex))
	else:
		request = req.Request(src+str(memberIndex)+'&page='+str(pageIndex))
		request.add_header('User-Agent', ua)
	try:
		with req.urlopen(request, timeout=3) as response:
			data = response.read().decode('utf-8')
	except urllib.error.URLError:
		print('something wrong, timed out') 
	root = bs4.BeautifulSoup(data,'html.parser')
	#print(root)
	#獲取此頁每一篇文章的連結
	articlesSrc = root.select('div.p-button__blog_detail a')
	#print(articlesSrc)
	if not articlesSrc and fatchBlogFlag:
		print('all finished, fatched empty blog')
		break
	time.sleep(3)
	while(fatchBlogFlag):
		print('\n\n\n\n')
		print('----------member index:'+str(memberIndex)+'page:'+str(pageIndex)+'----------')
		print('\n\n\n\n')
		#井口memberIndex:1
		if memberIndex == 0:
			#poka 專屬判斷
			request = req.Request(src+'000'+'&page='+str(pageIndex))
		else:
			request = req.Request(src+str(memberIndex)+'&page='+str(pageIndex))
			request.add_header('User-Agent', ua)
		with req.urlopen(request, timeout=3) as response:
			data = response.read().decode('utf-8')
		root = bs4.BeautifulSoup(data,'html.parser')
		#print(root)
		#獲取此頁每一篇文章的連結
		articlesSrc = root.select('div.p-button__blog_detail a')
		#print(articlesSrc)
		for artSRC in articlesSrc:
			print(artSRC['href'])

		if not articlesSrc:
			print('cant find more article')
			print('next member')
			break
		else:
			isDupicated = crawlArticle(articlesSrc,newBlogList)
			if isDupicated == 1:
				print('\n\n\n\n')
				print('----------member index:'+str(memberIndex)+'page:'+str(pageIndex)+' is dupicated----------')
				print('----------continue next member----------')
				print('\n\n\n\n')
				break
		#print(articles)
		pageIndex += 1
		print('pageIndex:',pageIndex)
	memberIndex += 1
	print('memberIndex:',memberIndex)
	fatchBlogFlag = True
	#if memberIndex == 25:
	#	print('新三期生blog memberIndex跳至1000')
	#	memberIndex = 1000
	#if memberIndex == 25:
	#	print('跳至Poka')
	#	memberIndex = 10000
	#if memberIndex == 37:
	#	print('跳至Poka')
	#	memberIndex = 10000
	#if memberIndex == 10001:
	#	print('跳至新四期生')
	#	memberIndex = 2000
print('更新blog',newBlogList)
newBlogList = list(dict.fromkeys(newBlogList))
print('更新blog',newBlogList)
print('--- %.2f seconds ---'%(time.time()-startTime))


