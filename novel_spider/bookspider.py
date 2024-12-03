import requests
from bs4 import BeautifulSoup
from ebooklib import epub
import os
from get_image_test import get_img
import time
from PIL import Image
import io
import pillow_avif

# os.chdir('./spider/novel_spider')

from decoder import decoder, get_encode_content, decode_css_content

headers = {
  "authority": "www.bilimanga.net",
  "method": "POST",
  "path": "/read/1/catalog",
  "scheme": "https",
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  "accept-encoding": "gzip, deflate, br, zstd",
  "accept-language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6",
  "cache-control": "no-cache",
  "content-length": "6616",
  "content-type": "application/x-www-form-urlencoded",
  "cookie": "jieqiVisitInfo=jieqiUserLogin%3D1729590509%2CjieqiUserId%3D88085; night=0; cf_chl_rc_m=1; __gads=ID=c21ea7abbbda123c:T=1728954122:RT=1733108421:S=ALNI_ManuS5bgx1Ool3JwkmVMuZjxo8OIw; __gpi=UID=00000f4337959d57:T=1728954122:RT=1733108421:S=ALNI_MaCUS4mioWA2xe_sC3sWTVgo4C9ew; __eoi=ID=e1694231e67c5903:T=1728954122:RT=1733108421:S=AA-AfjYrQrMWIz2zoJnKWwwEqH35; cf_clearance=E0yR8geM7FwNxfnol77Y_zz6vbVVgrqT7CNJLtLh9Ag-1733108598-1.2.1.1-eWcedS7qspWon4UyQXMu5u4GNjcFNBj9LnS4ZsnkQ4oLKxV0HGhpbEAD_P11S1lXi3rBsK.hwCE.PJ6I0bPaHmKaGfQk2K7BlS7fH7Shh2i7nlAGSVn9By41P82.76RhdU6SEIGxzHI5K3p0bEUY2w6gcP_BTucIWl3GmYnFTp22Ag_Nq7L1tC.0UGSqOL2zMVGPlJ6KjCVXh86g7tfSQAI8ZHjdbYNRs77PXhFU3tMVUPXio.YxtkhIvcqa7eNU3midTnV2uWXXmbSPq0deE7WMtADfcQ_evxslY_D8qGj5wjhOHtFLV7UspBsFoI3SBhAUqPH6LYLi0Sr64ChdUu642eeJeaAAifu_HNMPOEtf_q5ziXz8AVLpDq.D26RPN3O72YTI.F2DZjnwPTnUmt.jAmlDX8HuJwZkbwSSvn9mR2G36wJxsrzegBGTrPXi",
  "origin": "https://www.bilimanga.net",
  "pragma": "no-cache",
  "priority": "u=0, i",
  "referer": "https://www.bilimanga.net/read/1/catalog?__cf_chl_tk=spfLQhhfHncJnWGY.LEXb8TKvbq2edSCHcnS9jI5FHg-1733108629-1.0.1.1-lrhT4tRlzNh5nijeJcb1UiEnEU0pwK.ml_7G_.oUNM8",
  "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
  "sec-ch-ua-arch": "x86",
  "sec-ch-ua-bitness": "64",
  "sec-ch-ua-full-version": "131.0.6778.86",
  "sec-ch-ua-full-version-list": "\"Google Chrome\";v=\"131.0.6778.86\", \"Chromium\";v=\"131.0.6778.86\", \"Not_A Brand\";v=\"24.0.0.0\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-model": "",
  "sec-ch-ua-platform": "Windows",
  "sec-ch-ua-platform-version": "15.0.0",
  "sec-fetch-dest": "document",
  "sec-fetch-mode": "navigate",
  "sec-fetch-site": "same-origin",
  "sec-fetch-user": "?1",
  "upgrade-insecure-requests": "1",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


def catoon_spider(title, chapters, prefix='', author='佚名', cover=None):
  base_url = 'https://www.bilimanga.net'

  # 创建电子书
  book = epub.EpubBook()
  book.set_title(title)
  book.set_language('zh')
  book.add_author(author)

  if not cover == None:
    book_cover = get_img(cover)
    book.set_cover(f'{title}.jpg', book_cover)

  idx = 0
  tocs = []
  chapter_list = []
  for chapter in chapters:
    print('翻书等待。。。')
    time.sleep(1)
    path = chapter['link']
    if not path.startswith('/read'):
      continue
      
    # 获取HTML内容co
    url = base_url + path
    link = url

    chapter_name = chapter['title']

    total_content = ''
    i = 0
    while link:
      print('翻页等待。。。')
      time.sleep(1)
      # print('starting, geting response......')s
      response = requests.get(url, headers=headers)
      # print('got it')
      html_content = response.text
      # 解析HTML内容
      soup = BeautifulSoup(html_content, 'html.parser')
      catoon_content = soup.find(id="acontentz")  # 找到指定的div
      if catoon_content.find_all('img'):
        pic = catoon_content.find_all('img')
        for p in pic:
          p_path = p['data-src']
        # print(paragraphs[-1].text.encode('utf-8'))
        # content = "\n".join([(f'<p>{p.text}</p>') for p in paragraphs])

      images = catoon_content.find_all('img')
      for img in images:
        if img.has_key('data-src'):
          url = img['data-src']
        else:
          url = img['src']
        print(f'image -> {url} was downloading...')
        img_data = get_img(url)
        if url.endswith('.avif'):
          # 使用二进制数据创建一个字节流
          avif_stream = io.BytesIO(img_data)

          with Image.open(avif_stream) as img_p:
            # 将图片转换为 RGB 格式（因为 JPEG 不支持透明度）
            img_p = img_p.convert("RGB")
            
            # 创建一个新的字节流来保存转换后的 JPG 数据
            jpg_stream = io.BytesIO()
            img_p.save(jpg_stream, "JPEG")

            # 获取 JPG 的二进制数据
            img_data = jpg_stream.getvalue()

        # 添加图片到 EPUB 文件
        file_name = f"images/image{idx}_{i}.jpg"
        img_item = epub.EpubItem(uid=f"image{i}", file_name=file_name, media_type="image/jpeg", content=img_data)
        book.add_item(img_item)
        img['src'] = file_name
        i = i + 1
        

      for c in catoon_content.contents:
        if isinstance(c, str):
          total_content = total_content + c
        elif c.name == 'p':
          total_content = total_content + f'<p>{c.text}</p>'
        elif c.name == 'img':
          img_content = f'<img class="imagecontent" src="{c['src']}"/>'
          total_content = total_content + img_content
        elif c.name == 'br':
          # print('br')
          pass
        else:
          # print('unknown')
          pass

      link = soup.find('a', text='下一页')
      if not link == None:
        link = link['href']
        print(link)
        url = base_url + link
        print('下一页')
        

    chapter = epub.EpubHtml(title=chapter_name, file_name=f'chapter_{idx}.xhtml', lang='zh')
    chapter.content = f'<html><body><h1>{chapter_name}</h1><div id="TextContent">{total_content}</div></body></html>'
    book.add_item(chapter)
    tocs.append(epub.Link(f'chapter_{idx}.xhtml', chapter_name, f'chapter_{idx}'))
    idx = idx + 1
    chapter_list.append(chapter)
    print('下一章')
    
  print(f'{title} 爬取完成，保存中。。。')
  # 目录和样式
  book.toc = tuple(tocs)
  book.spine = ['nav'] + chapter_list
  print(f'bookspine {book.spine}')
  book.add_item(epub.EpubNcx())
  book.add_item(epub.EpubNav())


  # 保存成epub文件
  save_path = os.path.join('.', prefix, f'{prefix}-{title}.epub')
  epub.write_epub(save_path, book)
  print(f'{save_path} 保存成功。')



def book_spider(title, chapters, prefix='', author='佚名', cover=None):
  base_url = 'https://www.linovelib.com'
  

  # 创建电子书
  book = epub.EpubBook()
  book.set_title(title)
  book.set_language('zh')
  book.add_author(author)

  if not cover == None:
    book_cover = get_img(cover)
    book.set_cover(f'{title}.jpg', book_cover)

  idx = 0
  tocs = []
  chapter_list = []
  for chapter in chapters:
    print('翻书等待。。。')
    time.sleep(3)
    path = chapter['link']
    if not path.startswith('/novel'):
      continue
      
    # 获取HTML内容co
    url = base_url + path
    link = url

    chapter_name = chapter['title']

    total_content = ''
    i = 0
    while link:
      print('翻页等待。。。')
      time.sleep(1)
      # print('starting, geting response......')s
      response = requests.get(url, headers=headers)
      # print('got it')
      html_content = response.text
      # 解析HTML内容
      soup = BeautifulSoup(html_content, 'html.parser')
      text_content = soup.find(id="TextContent")  # 找到指定的div
      if text_content.find_all('p'):
        paragraphs = text_content.find_all('p')  # 获取所有的<p>标签中的内容
        for p in paragraphs:
          p.string = decoder(p.text)
        # print(paragraphs[-1].text.encode('utf-8'))
        # content = "\n".join([(f'<p>{p.text}</p>') for p in paragraphs])


        # 查找所有 <style> 标签
        style_tags = soup.find_all('style')
        # 指定要查找的 CSS 内容
        target_css = """@font-face"""
        # 初始化标志变量
        found = False

        # 遍历所有 <style> 标签，检查内容
        for style_tag in style_tags:
            if target_css in style_tag.string:
                found = True
                break
        # 输出结果
        if found:
            print("HTML 页面中存在指定的 <style> 内容")
            get_encode_content(paragraphs[-1].text)
            d = decode_css_content(paragraphs[-1].text)
            paragraphs[-1].string = d

        else:
            print("HTML 页面中不存在指定的 <style> 内容")

      images = text_content.find_all('img')
      for img in images:
        if img.has_key('data-src'):
          url = img['data-src']
        else:
          url = img['src']
        print(f'image -> {url} was downloading...')
        img_data = get_img(url)
        # 添加图片到 EPUB 文件
        file_name = f"images/image{idx}_{i}.jpg"
        img_item = epub.EpubItem(uid=f"image{idx}_{i}", file_name=file_name, media_type="image/jpeg", content=img_data)
        book.add_item(img_item)
        img['src'] = file_name
        i = i + 1
        

      for c in text_content.contents:
        if isinstance(c, str):
          total_content = total_content + c
        elif c.name == 'p':
          total_content = total_content + f'<p>{c.text}</p>'
        elif c.name == 'img':
          img_content = f'<img class="imagecontent" src="{c['src']}"/>'
          total_content = total_content + img_content
        elif c.name == 'br':
          # print('br')
          pass
        else:
          # print('unknown')
          pass

      link = soup.find('a', text='下一页')
      if not link == None:
        link = link['href']
        print(link)
        url = base_url + link
        print('下一页')
        

    chapter = epub.EpubHtml(title=chapter_name, file_name=f'chapter_{idx}.xhtml', lang='zh')
    chapter.content = f'<html><body><h1>{chapter_name}</h1><div id="TextContent">{total_content}</div></body></html>'
    book.add_item(chapter)
    tocs.append(epub.Link(f'chapter_{idx}.xhtml', chapter_name, f'chapter_{idx}'))
    idx = idx + 1
    chapter_list.append(chapter)
    print('下一章')
    
  print(f'{title} 爬取完成，保存中。。。')
  # 目录和样式
  book.toc = tuple(tocs)
  book.spine = ['nav'] + chapter_list
  print(f'bookspine {book.spine}')
  book.add_item(epub.EpubNcx())
  book.add_item(epub.EpubNav())


  # 保存成epub文件
  save_path = os.path.join('.', prefix, f'{prefix}-{title}.epub')
  epub.write_epub(save_path, book)
  print(f'{save_path} 保存成功。')

def catalog_parse(url):
  # response = requests.get(url, headers=headers)
  # html_content = response.text
  html_content = '''
  <!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>葬送的芙莉蓮漫畫_葬送者芙莉蓮, 葬送のフリーレン漫畫線上看_山田鐘人作品_奇幻冒險漫畫_嗶哩漫畫</title>
<meta name="keywords" content="葬送的芙莉蓮,葬送者芙莉蓮, 葬送のフリーレン,山田鐘人,奇幻冒險漫畫,在線漫畫,看漫畫,嗶哩漫畫" />
<meta name="description" content="葬送的芙莉蓮(葬送者芙莉蓮, 葬送のフリーレン)內容簡介：在勇者死後仍舊活著的精靈魔法使·芙莉蓮。
她再次沿著過去與勇者們一起冒險的旅途前進。
替過去與現在的旅途增添色彩的是…各種無法取代的邂逅與活動——
故事描述她陸續想起與勇者們的日常。
由英雄們的記憶所..." />
<meta name="applicable-device" content="mobile" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="viewport" content="initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0,user-scalable=0,width=device-width" />
<meta name="theme-color" content="#232323" media="(prefers-color-scheme: dark)" />
<link rel="stylesheet" href="https://www.bilimanga.net/themes/mobile/css/info.css">
<script src="https://www.bilimanga.net/themes/mobile/js/jquery-3.3.1.js"></script>
<script type="text/javascript" src="/scripts/darkmode.js"></script>
<script src="https://www.bilimanga.net/themes/mobile/js/core.js"></script>
<script async src="https://www.bilimanga.net/themes/mobile/js/lazysizes.min.js"></script>
<script type="text/javascript" src="https://www.bilimanga.net/scripts/common.js?v0922a3" charset="UTF-8"></script>
<style>.btn-group-tab .active {padding: 1rem; line-height: 1.3; white-space: normal; word-wrap: break-word; word-break: keep-all; text-overflow: ellipsis; display: -webkit-box; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 10px;}</style><script>var bookinfo = {mangaid:'1'};</script>
</head>
<body>
<script src="https://www.bilimanga.net/themes/mobile/js/sprite.js"></script>
<div class="page page-chapter">
	<div class="content">
		<header id="header" class="header"><a href="/detail/1.html" class="header-back jsBack"><svg class="icon icon-arrow-l"><title>返回</title><use xlink:href="#icon-arrow-l"></use></svg></a>
		<!--<span class="header-back-title">葬送的芙莉蓮</span>-->
		<div class="header-operate">
			<a id="openSearchPopup" href="javascript:" class="icon icon-search" title="搜索"><svg><use xlink:href="#icon-search"></use></svg></a><a id="openGuide" href="javascript:" class="icon icon-more" title="更多" data-rel="guide"></a>
		</div>
		</header>
				<!-- 更多內容的導航 S -->
<div id="guide" class="guide">
	<i id="guideOverlay1" class="guide-overlay"></i>
	<div class="guide-content">
		<nav class="guide-nav">
		<a href="/" class="guide-nav-a">
		<i class="icon icon-home"></i>
		<h4 class="guide-nav-h">首頁</h4>
		</a>
		<a href="/alltopics" class="guide-nav-a">
		<i class="icon icon-sort"></i>
		<h4 class="guide-nav-h">圈子</h4>
		</a>
		<a href="/top.html" class="guide-nav-a">
		<i class="icon icon-rank"></i>
		<h4 class="guide-nav-h">排行榜</h4>
		</a>
		<a href="/filter/" class="guide-nav-a">
		<i class="icon icon-fuli"></i>
		<h4 class="guide-nav-h">漫畫</h4>
		</a>
		<a href="/topfull/postdate/1.html" class="guide-nav-a">
		<i class="icon icon-end"></i>
		<h4 class="guide-nav-h">完本</h4>
		</a>
		<a href="/user.php" class="guide-nav-a ">
		<i class="icon icon-account"></i>
		<h4 class="guide-nav-h">會員</h4>
		</a>
		</nav>
		<div class="guide-footer">
		<a href="/bookcase.php" class="btn-primary" data-size="14">漫畫收藏</a>
		</div>
	</div>
</div>
<!-- 更多內容的導航 E -->
<!-- 公用頭部 E -->
		<div id="catalogWrapper">
			<div id="chapterNav" class="btn-group-tab">
				<nav class="btn-group">
				<h1 class="btn-group-cell book-title btn-blank active">葬送的芙莉蓮</h1>
				</nav>
			</div>
			<div class="module module-merge">
				<!-- 目錄頁內容 -->
				<div id="catelogX" class="chapter-tab-x active">
					<div class="module-header">
						<div class="module-header-l">
							<h4 class="chapter-sub-title">最後更新<span class="char-dot">:</span>2024-11-24<span class="char-dot">·</span>共<output>152</output>話</h4>
						</div>
						<div class="module-header-r">
							<a id="reverse" href="javascript:" class="module-header-btn dark">倒序</a>
						</div>
					</div>
					<div id="volumes" class="chapter-ol chapter-ol-catalog">
					<div id="bookmarkX" class="chapter-tab-x"><script src="https://www.bilimanga.net/themes/mobile/js/newread.js?v7.29a1"></script></div>
						
						
						
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第１卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/2.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/1.jpg" alt="葬送的芙莉蓮 第１卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/2.html" class="chapter-li-a "><span class="chapter-index ">第01話 冒險結束</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/3.html" class="chapter-li-a "><span class="chapter-index ">第02話 僧侶的謊言</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/4.html" class="chapter-li-a "><span class="chapter-index ">第03话 蒼月草</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/5.html" class="chapter-li-a "><span class="chapter-index ">第04话 魔法使的秘密</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/6.html" class="chapter-li-a "><span class="chapter-index ">第05话 殺人魔法</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/7.html" class="chapter-li-a "><span class="chapter-index ">第06話 新年祭</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/8.html" class="chapter-li-a "><span class="chapter-index ">第07話 靈魂長眠之地</span></a></li>
						</ul></div><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9191420394554172"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-9191420394554172"
     data-ad-slot="1548926638"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script><script>!function(){function f(){var a=document.getElementById("volumes");a.innerHTML='<div class="d-note"><p>\u0028\u0026\u0023\u0032\u0034\u0033\u003b\ufe4f\u0026\u0023\u0032\u0034\u0032\u003b\uff61\u0029</p><p>\u62b1\u6b49\uff0c\u67ef\u5357\u4fa6\u6d4b\u5230\u60a8\u5df2\u6fc0\u6d3b\u5e7f\u544a\u62e6\u622a\u5668\u3002</p><p>\u8bf7\u8003\u8651\u901a\u8fc7\u7981\u7528\u60a8\u7684\u5e7f\u544a\u62e6\u622a\u5668\u6765\u5e2e\u52a9\u6211\u4eec\u7ef4\u62a4\u672c\u7f51\u7ad9\u3002</p><p>\u7ee7\u7eed\u67e5\u770b\u5185\u5bb9\uff0c\u8bf7\u7981\u7528\u5e7f\u544a\u62e6\u622a\u5668\u0020\u6216\u0020\u5c06\u672c\u7ad9\u52a0\u5165\u5e7f\u544a\u62e6\u622a\u5668\u767d\u540d\u5355\uff0c\u5e76\u5237\u65b0\u9875\u9762\u3002</p><p>\u8c22\u8c22\uff01\uff01\uff01</p></div>'}var b=document.createElement("script");b.type="text/javascript";b.async=!0;b.src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js";b.onerror=function(){f();window.adblock=!0};var e=document.getElementsByTagName("script")[0];e.parentNode.insertBefore(b,e)}();</script>
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第２卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/130.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/2040.jpg" alt="葬送的芙莉蓮 第２卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/130.html" class="chapter-li-a "><span class="chapter-index ">第08話 百分之一</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/131.html" class="chapter-li-a "><span class="chapter-index ">第09話 死者的幻影</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/132.html" class="chapter-li-a "><span class="chapter-index ">第10話 紅鏡龍</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/133.html" class="chapter-li-a "><span class="chapter-index ">第11話 村子的英雄</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/134.html" class="chapter-li-a "><span class="chapter-index ">第12話 北方的哨所</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/135.html" class="chapter-li-a "><span class="chapter-index ">第13話 解放祭</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/136.html" class="chapter-li-a "><span class="chapter-index ">第14話 說話的魔物</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/137.html" class="chapter-li-a "><span class="chapter-index ">第15話 多拉特</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/138.html" class="chapter-li-a "><span class="chapter-index ">第16話 殺死衛兵</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/139.html" class="chapter-li-a "><span class="chapter-index ">第17話 葬送的芙莉蓮</span></a></li>
						</ul></div>
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第３卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/141.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/2249.jpg" alt="葬送的芙莉蓮 第３卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/141.html" class="chapter-li-a "><span class="chapter-index ">第18話 不死軍團</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/142.html" class="chapter-li-a "><span class="chapter-index ">第19話 突襲</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/143.html" class="chapter-li-a "><span class="chapter-index ">第20話 師父的招式</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/144.html" class="chapter-li-a "><span class="chapter-index ">第21話 卑鄙小人</span></a></li>
					<li class="chapter-li jsChapter"><a href="javascript:cid(1)" class="chapter-li-a "><span class="chapter-index ">第22話 服從的天平</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/146.html" class="chapter-li-a "><span class="chapter-index ">第23話 勝利與弔唁</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/147.html" class="chapter-li-a "><span class="chapter-index ">第24話 精靈的願望</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/148.html" class="chapter-li-a "><span class="chapter-index ">第25話 劍之村</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/149.html" class="chapter-li-a "><span class="chapter-index ">第26話 給戰士的禮物</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/150.html" class="chapter-li-a "><span class="chapter-index ">第27話 平凡村子的僧侶</span></a></li>
						</ul></div>
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第４卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/152.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/2460.jpg" alt="葬送的芙莉蓮 第４卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/152.html" class="chapter-li-a "><span class="chapter-index ">第28話 僧侶與後悔</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/153.html" class="chapter-li-a "><span class="chapter-index ">第29話 理想中的大人</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/154.html" class="chapter-li-a "><span class="chapter-index ">第30話 鏡蓮華</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/155.html" class="chapter-li-a "><span class="chapter-index ">第31話 混沌花</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/156.html" class="chapter-li-a "><span class="chapter-index ">第32話 歐爾登家</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/157.html" class="chapter-li-a "><span class="chapter-index ">第33話 弗爾爺爺</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/158.html" class="chapter-li-a "><span class="chapter-index ">第34話 英雄之像</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/159.html" class="chapter-li-a "><span class="chapter-index ">第35話 踏上旅途的契機</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/160.html" class="chapter-li-a "><span class="chapter-index ">第36話 心靈支柱</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/161.html" class="chapter-li-a "><span class="chapter-index ">第37話 一級測驗</span></a></li>
						</ul></div>
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第５卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/163.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/2659.jpg" alt="葬送的芙莉蓮 第５卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/163.html" class="chapter-li-a "><span class="chapter-index ">第38話 隕鐵鳥(Stille)</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/164.html" class="chapter-li-a "><span class="chapter-index ">第39話 啟動捕捉作戰</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/165.html" class="chapter-li-a "><span class="chapter-index ">第40話 抓住鳥的魔法</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/166.html" class="chapter-li-a "><span class="chapter-index ">第41話 下定決心的時間</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/167.html" class="chapter-li-a "><span class="chapter-index ">第42話 戰鬥的理由</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/168.html" class="chapter-li-a "><span class="chapter-index ">第43話 特權</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/169.html" class="chapter-li-a "><span class="chapter-index ">第44話 奪回鐵鳥(Stille)</span></a></li>
					<li class="chapter-li jsChapter"><a href="javascript:cid(1)" class="chapter-li-a "><span class="chapter-index ">第45話 操控水的魔法</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/171.html" class="chapter-li-a "><span class="chapter-index ">第46話 更加M味的味道</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/172.html" class="chapter-li-a "><span class="chapter-index ">第47話 費倫與烘焙點心</span></a></li>
						</ul></div>
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第６卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/174.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/2856.jpg" alt="葬送的芙莉蓮 第６卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/174.html" class="chapter-li-a "><span class="chapter-index ">第48話 零落的王墓</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/175.html" class="chapter-li-a "><span class="chapter-index ">第49話 迷宮與魔導具</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/176.html" class="chapter-li-a "><span class="chapter-index ">第50話 永鏡的蕙魔(Spiegel)</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/177.html" class="chapter-li-a "><span class="chapter-index ">第51話 迷宫戰鬥</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/178.html" class="chapter-li-a "><span class="chapter-index ">第52話 作戰會議</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/179.html" class="chapter-li-a "><span class="chapter-index ">第53話 人類的時代</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/180.html" class="chapter-li-a "><span class="chapter-index ">第54話 大概什麼都能砍的魔法</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/181.html" class="chapter-li-a "><span class="chapter-index ">第55話 第二次測驗結東</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/182.html" class="chapter-li-a "><span class="chapter-index ">第56話 費倫的法杖</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/183.html" class="chapter-li-a "><span class="chapter-index ">第57話 第三次測驗</span></a></li>
						</ul></div>
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第７卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/185.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/3046.jpg" alt="葬送的芙莉蓮 第７卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/185.html" class="chapter-li-a "><span class="chapter-index ">第58話 賽莉耶的直覺</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/186.html" class="chapter-li-a "><span class="chapter-index ">第59話 微不是道的善行</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/187.html" class="chapter-li-a "><span class="chapter-index ">第60話 踏上旅途與別離</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/188.html" class="chapter-li-a "><span class="chapter-index ">第61話 封魔礦</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/189.html" class="chapter-li-a "><span class="chapter-index ">第62話 踏上旅途的理由</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/190.html" class="chapter-li-a "><span class="chapter-index ">第63話 南方勇者</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/191.html" class="chapter-li-a "><span class="chapter-index ">第64話 劍之魔族</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/192.html" class="chapter-li-a "><span class="chapter-index ">第65話 艾托瓦斯山的秘湯</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/193.html" class="chapter-li-a "><span class="chapter-index ">第66話 喜歡的地方</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/194.html" class="chapter-li-a "><span class="chapter-index ">第67話 悠閒的時光</span></a></li></ul></div>
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第８卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/196.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/3232.jpg" alt="葬送的芙莉蓮 第８卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/196.html" class="chapter-li-a "><span class="chapter-index ">第68話 北部高原</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/197.html" class="chapter-li-a "><span class="chapter-index ">第69話 皇帝酒(Boshafl)</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/198.html" class="chapter-li-a "><span class="chapter-index ">第70話 諾姆商會</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/199.html" class="chapter-li-a "><span class="chapter-index ">第71話 討伐委託</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/200.html" class="chapter-li-a "><span class="chapter-index ">第72話 將軍</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/201.html" class="chapter-li-a "><span class="chapter-index ">第73話 遭遇戰</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/202.html" class="chapter-li-a "><span class="chapter-index ">第74話 神技的雷沃戴</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/203.html" class="chapter-li-a "><span class="chapter-index ">第75話 讓霧消散的魔法</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/204.html" class="chapter-li-a "><span class="chapter-index ">第76話 結束</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/205.html" class="chapter-li-a "><span class="chapter-index ">第77話 龍的群體</span></a></li>
						</ul></div>
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第９卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/207.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/3422.jpg" alt="葬送的芙莉蓮 第９卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/207.html" class="chapter-li-a "><span class="chapter-index ">第78話 柯利多亞湖</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/208.html" class="chapter-li-a "><span class="chapter-index ">第79話 托亞大溪谷</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/209.html" class="chapter-li-a "><span class="chapter-index ">第80話 聖雪結晶</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/210.html" class="chapter-li-a "><span class="chapter-index ">第81話 黃金郷</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/211.html" class="chapter-li-a "><span class="chapter-index ">第82話 將萬物變成黃金的魔法</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/212.html" class="chapter-li-a "><span class="chapter-index ">第83話 控制的石環</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/213.html" class="chapter-li-a "><span class="chapter-index ">第84話 不知死活的人</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/214.html" class="chapter-li-a "><span class="chapter-index ">第85話 惡意</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/215.html" class="chapter-li-a "><span class="chapter-index ">第86話 協商</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/216.html" class="chapter-li-a "><span class="chapter-index ">第87話 好感</span></a></li>
						</ul></div>
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第10卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/218.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/3612.jpg" alt="葬送的芙莉蓮 第10卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/218.html" class="chapter-li-a "><span class="chapter-index ">第88話 索利泰爾</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/219.html" class="chapter-li-a "><span class="chapter-index ">第89話 罪惡感</span></a></li>
					<li class="chapter-li jsChapter"><a href="javascript:cid(1)" class="chapter-li-a "><span class="chapter-index ">第90話 古留克</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/221.html" class="chapter-li-a "><span class="chapter-index ">第91話 站上檯面</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/222.html" class="chapter-li-a "><span class="chapter-index ">第92話 瓦伊澤的終結</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/223.html" class="chapter-li-a "><span class="chapter-index ">第93話 大結界</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/224.html" class="chapter-li-a "><span class="chapter-index ">第94話 解析</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/225.html" class="chapter-li-a "><span class="chapter-index ">第95話 無名的大魔族</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/226.html" class="chapter-li-a "><span class="chapter-index ">第96話 師徒</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/227.html" class="chapter-li-a "><span class="chapter-index ">第97話 觀測</span></a></li>
						</ul></div>
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第11卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/229.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/3806.jpg" alt="葬送的芙莉蓮 第11卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/229.html" class="chapter-li-a "><span class="chapter-index ">第98話 報應</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/230.html" class="chapter-li-a "><span class="chapter-index ">第99話 攻防</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/231.html" class="chapter-li-a "><span class="chapter-index ">第100話 魔法使的基礎</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/232.html" class="chapter-li-a "><span class="chapter-index ">第101話 解決對策</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/233.html" class="chapter-li-a "><span class="chapter-index ">第102話 不分勝負</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/234.html" class="chapter-li-a "><span class="chapter-index ">第103話 報應的時刻</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/235.html" class="chapter-li-a "><span class="chapter-index ">第104話 掃墓</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/236.html" class="chapter-li-a "><span class="chapter-index ">第105話 哥列姆</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/237.html" class="chapter-li-a "><span class="chapter-index ">第106話 天脈龍</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/238.html" class="chapter-li-a "><span class="chapter-index ">第107話 N神的石碑</span></a></li>
						</ul></div>
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第12卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/240.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/382165.avif" alt="葬送的芙莉蓮 第12卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/240.html" class="chapter-li-a "><span class="chapter-index ">第108話 重逢</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/241.html" class="chapter-li-a "><span class="chapter-index ">第109話 殘影崔爾特</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/242.html" class="chapter-li-a "><span class="chapter-index ">第110話 勇者一行人</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/243.html" class="chapter-li-a "><span class="chapter-index ">第111話 護衛委託</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/244.html" class="chapter-li-a "><span class="chapter-index ">第112話 信賴</span></a></li>
					<li class="chapter-li jsChapter"><a href="javascript:cid(1)" class="chapter-li-a "><span class="chapter-index ">第113話 皇獄龍</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/246.html" class="chapter-li-a "><span class="chapter-index ">第114話 勇者之劍</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/247.html" class="chapter-li-a "><span class="chapter-index ">第115話 好朋友</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/248.html" class="chapter-li-a "><span class="chapter-index ">第116話 歸還的魔法</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/249.html" class="chapter-li-a "><span class="chapter-index ">第117話 奇蹟的幻影</span></a></li>
						</ul></div>
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第13卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/251.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/382362.avif" alt="葬送的芙莉蓮 第13卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/251.html" class="chapter-li-a "><span class="chapter-index ">第118話 菲亞拉托爾</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/252.html" class="chapter-li-a "><span class="chapter-index ">第119話 回憶</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/253.html" class="chapter-li-a "><span class="chapter-index ">第120話 虛像英雄</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/254.html" class="chapter-li-a "><span class="chapter-index ">第121話 街道上的魔物</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/255.html" class="chapter-li-a "><span class="chapter-index ">第122話 提坦城堡</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/256.html" class="chapter-li-a "><span class="chapter-index ">第123話 努力至今的證明</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/257.html" class="chapter-li-a "><span class="chapter-index ">第124話 影子戰士</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/258.html" class="chapter-li-a "><span class="chapter-index ">第125話 家人</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/259.html" class="chapter-li-a "><span class="chapter-index ">第126話 全新的任務</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/260.html" class="chapter-li-a "><span class="chapter-index ">第127話 回收任務</span></a></li>
						</ul></div>
					<div class="catalog-volume"><ul class="volume-chapters">
					<li class="chapter-bar chapter-li"><h3>第14卷</h3></li><li class="volume-cover chapter-li"><a href="/read/1/262.html" class="volume-cover-img"><img src="/images/book-cover-no.svg" data-src="https://i.motiezw.com/cover/1/4362.jpg" alt="葬送的芙莉蓮 第14卷" class="lazyload" /></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/262.html" class="chapter-li-a "><span class="chapter-index ">第128話 廢導特多隊</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/263.html" class="chapter-li-a "><span class="chapter-index ">第129話 帝國之影</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/264.html" class="chapter-li-a "><span class="chapter-index ">第130話 水面之下</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/6888.html" class="chapter-li-a "><span class="chapter-index ">第131話 逃跑</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/31265.html" class="chapter-li-a "><span class="chapter-index ">第132話</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/31266.html" class="chapter-li-a "><span class="chapter-index ">第133話</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/31267.html" class="chapter-li-a "><span class="chapter-index ">第134話</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/31268.html" class="chapter-li-a "><span class="chapter-index ">第135話</span></a></li>
					<li class="chapter-li jsChapter"><a href="javascript:cid(1)" class="chapter-li-a "><span class="chapter-index ">第136話</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/34945.html" class="chapter-li-a "><span class="chapter-index ">第137話</span></a></li>
					<li class="chapter-li jsChapter"><a href="/read/1/34946.html" class="chapter-li-a "><span class="chapter-index ">第138話</span></a></li>
					</ul></div>
				</div>
			</div>
		</div>
	</div>
</div>
<style>.d-note {height: 70vh;font-size:1rem;font-weight:400;line-height:1.5; position:relative;padding:0.75rem 1.25rem;margin-bottom:1rem;border:1px solid transparent;}.d-note p {word-wrap:break-word;text-indent:2em;margin-bottom:0.1rem;}</style>
<script>var jieqiVisitedLinks=localStorage.getItem('jieqiVisitedLinks');var visitedLinks=[];if(jieqiVisitedLinks){visitedLinks=JSON.parse(jieqiVisitedLinks)}var chapterLinks=document.querySelectorAll('#volumes .jsChapter a');chapterLinks.forEach(function(a){var href=a.getAttribute('href');var mangaId=extractMangaId(href);var chapterId=extractChapterId(href);var visited=visitedLinks.some(function(link){return link.mangaid===mangaId&&link.chapterid===chapterId});if(visited){a.classList.add('visited')}});function extractMangaId(href){var match=href.match(/\/read\/(\d+)\/(\d+).html/);return match?match[1]:null}function extractChapterId(href){var match=href.match(/\/read\/(\d+)\/(\d+).html/);return match?match[2]:null}</script>
<a href="#" class="footer-backtop-circle jsBackToTop" title="返回頂部"><svg class="icon icon-backtop"><use xlink:href="#icon-backtop"></use></svg></a>
<footer class="footer">
  <div class="footer-link fuli-footer-link">
	<a href="/bookcase.php" class="footer-link-a dark">書架</a>
	<a href="/report.php" class="footer-link-a dark">反饋</a>
	<a href="/help.html" class="footer-link-a dark">幫助</a>
	<a href="javascript:" class="footer-link-a dark">简体</a>
	<a href="javascript:" class="footer-link-a dark" id="app"><b>客戶端</b></a>
	</div>
  <div class="footer-copy">Copyright &copy; 2024 嗶哩漫畫</div></footer>
<div id="searchPopup" class="search-popup" style="display: none;">
  <header class="header">
	<form id="searchForm" action="https://www.bilimanga.net/search.html" class="search-form">
	  <div class="search-area">
		<svg class="icon icon-search">
		  <use xlink:href="#icon-search"></use>
		</svg>
		<input autofocus="autofocus" id="searchkey" type="text" name="searchkey" class="search-input" value="" autocomplete="off">
		<button id="clearSearchKeyword" type="button" class="search-reset" hidden>
		  <i class="icon icon-clear">
			<svg>
			  <use xlink:href="#icon-clear"></use>
			</svg>
		  </i>
		</button>
	  </div>
	  <a id="closeSearchPopup" href="javascript:" class="search-cancel">取消</a></form>
  </header>
  <div id="searchHotHistory" class="search-hot-history">
	<div id="searchPopularWords" class="search-popular loading-animation" style="overflow:hidden;transition:height .2s ease 0s;height:auto">
	  <div class="search-title-bar">
		<h5 class="search-title">大家都在搜</h5></div>
	  <div class="search-tags">
				<a href="/detail/1.html" class="btn-line-gray jsSearchLink">葬送的芙莉蓮</a>

				<a href="/detail/2.html" class="btn-line-gray jsSearchLink">【我推的孩子】</a>

				<a href="/detail/3.html" class="btn-line-gray jsSearchLink">關於鄰家的天使大人不知不覺把我慣成廢人這檔子事</a>

				<a href="/detail/4.html" class="btn-line-gray jsSearchLink">轉生成蜘蛛又怎樣！</a>

				<a href="/detail/5.html" class="btn-line-gray jsSearchLink">冰菓</a>

				<a href="/detail/6.html" class="btn-line-gray jsSearchLink">香格里拉・開拓異境 ～糞作獵手挑戰神作～</a>

				<a href="/detail/7.html" class="btn-line-gray jsSearchLink">七龍珠 (全彩文傳版)</a>

				<a href="/detail/8.html" class="btn-line-gray jsSearchLink">安達與島村 (重製版)</a>
</div><hr><div class="searchtip">支持 <b>書名</b><b>作者</b><b>主題</b><b>譯者</b><br><p class="red">支持简体字搜索</p><br><div>如果不記得書名，請輸入關鍵詞進行搜索<br>比如：青春｜異世界｜豬頭少年</div></div></div>
  </div>
  <style>.searchtip{padding: 1.2em;}.searchtip b{background: #ff9800; color: #fff; margin: 0 3px 0 0; padding: 2px 15px; font-size: .825rem; border-radius: 30px; font-weight: 400;}/*@font-face{font-family:read; font-display:block; src: url('/public/font/read.woff2') format('woff2'), url('/public/font/read.ttf') format('truetype');}.jsBack{font-family: "read" !important;}*/</style>
</div>

<script>
  if ('serviceWorker' in navigator) {
	  navigator.serviceWorker.getRegistrations().then(function(registrations) {
		for (let registration of registrations) {
		  registration.unregister();
		}
	  });
  }
</script>
</body>
</html>
  '''
  # 解析HTML内容
  soup = BeautifulSoup(html_content, 'html.parser')

  # 获取所有的卷信息
  volumes = soup.find_all('div', class_='catalog-volume')

  volume_list = []
  # 分别提取每一卷的内容
  for volume in volumes:
      # 提取卷标题
      volume_title = volume.find('h3').text
      print(f"\n{volume_title}")
      v_dict = {}
      v_dict['title'] = volume_title
      c_list = []
      volume_cover = None
      if not volume.find('li', class_='volume-cover') == None:
        volume_cover = volume.find('li', class_='volume-cover').find('img')['data-src']
      v_dict['cover'] = volume_cover

      # 提取卷中的章节链接和文本
      chapters = volume.find_all('li', class_='jsChapter')
      for chapter in chapters:
          link = chapter.find('a')['href']
          text = chapter.find('a').text
          print(f"Link: {link}, Text: {text}")
          cc = {}
          cc['title'] = text
          cc['link'] = link
          c_list.append(cc)
      v_dict['chapters'] = c_list
      volume_list.append(v_dict)
  return volume_list

if __name__=='__main__':
  url = 'https://www.bilimanga.net/read/1/catalog'
  volume_list = catalog_parse(url)
  print(f'total {len(volume_list)}')
  
  dir_name = '葬送的芙莉莲'
  author_name = '山田鐘人'
  if not os.path.exists(dir_name):
    os.mkdir(dir_name)

  start_with = 14
  
  i = 1
  for volume in volume_list:
    if i < start_with:
      i = i + 1
      continue
    title = dir_name + '-' + volume['title']
    cover = volume['cover']
    chapters = volume['chapters']
    print(f'{title} was downloading...')
    print(chapters)
    catoon_spider(title, chapters, dir_name, author_name, cover)