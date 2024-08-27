import requests
from bs4 import BeautifulSoup
from ebooklib import epub
import os
from get_image_test import get_img
import time

# os.chdir('./spider/novel_spider')

from decoder import decoder, get_encode_content, decode_css_content

headers = {
    "authority": "www.linovelib.com",
    "method": "GET",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cookie": "Hm_lvt_ef8d5b3eafdfe7d1bbf72e3f450ad2ed=1724142484; HMACCOUNT=5AF594564CA7E69D; Hm_lpvt_ef8d5b3eafdfe7d1bbf72e3f450ad2ed=1724142772; __gads=ID=ba5fb523599a56d1:T=1721186733:RT=1724143049:S=ALNI_MZWTE_wbN7fpT81AQSpGehl6iHxEg; __gpi=UID=00000e96b9c535d1:T=1721186733:RT=1724143049:S=ALNI_Ma5HZTe3YyOL6-y3WwPREcJ6HUL4g; __eoi=ID=ab3cb9994e464ee3:T=1721186733:RT=1724143049:S=AA-AfjZhf0Zd3ww9r-70au9HD-0I; jieqiRecentRead=2154.77226.0.1.1724139523.0-41.117265.0.1.1724142482.0; cf_clearance=_kq7.4_2EXsxFnHByhZig4nVvzFhJM2d1qLTFyutAHw-1724143138-1.2.1.1-67BL9TvWF1ezwnsRJvZCPu7Itr1ZPo_GQneaD8k1PJc_IUiDtPPtIhh9E4qRuRhct1iSaTKW7Mt4cMDoKZLp6xHUoIrHdNa4pDWu0OX5SEw1PSmGrVQPab3AGHKge1Vg0wFY_VP2VKAg7X_kceL14Crsn_FPEt57HMfwCXhpEhUk5uHnYfuOYvzI7J.yQQ23V0D.eHbwHBMTqqJHtb9PZDchjG28mrjN_xOCOSupf7YgjkGeB.E8x0.9jCjNYx6ZTmlyc0bhiZrbJonmDkw2SzOqtxcExs5j58zd.DtpAWm0J5oQKIcdXmm.cspyDx8P3JBVlncEElvKemvbsrhArVSfwq9.jnR8c86eMXMv60IhdunnXlsc3rPIiKsg54RPf7bUvGQGuOXyfaRNC0olfg; FCNEC=%5B%5B%22AKsRol-6lCVic-bNvEYSXRSu01EFLn8Zb3UJ75UnRMpeq2fJHU4J1odMCsBoTAYXmDtkfPQV1TsgI_IRmkwq7lyVr1Yi0uG1rKgT_AoBTXHhguHuV76lynrZYQymaJ9MPwC9FAN3UAji7kGylWSaJOvZUQkx7JGyYg%3D%3D%22%5D%5D",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
  }

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
        img_item = epub.EpubItem(uid=f"image{i}", file_name=file_name, media_type="image/jpeg", content=img_data)
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
  response = requests.get(url, headers=headers)
  html_content = response.text
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
  url = 'https://www.bilinovel.com/novel/184/catalog'
  volume_list = catalog_parse(url)
  print(f'total {len(volume_list)}')
  
  dir_name = '空之境界'
  author_name = '奈须蘑菇'
  if not os.path.exists(dir_name):
    os.mkdir(dir_name)

  start_with = 1
  i = 1
  for volume in volume_list:
    if i < start_with:
      i = i + 1
      continue
    title = volume['title']
    cover = volume['cover']
    chapters = volume['chapters']
    print(f'{title} was downloading...')
    print(chapters)
    book_spider(title, chapters, dir_name, author_name, cover)