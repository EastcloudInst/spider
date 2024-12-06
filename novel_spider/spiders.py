import requests
from ebooklib import epub
from utils import *
import time
from PIL import Image
import io, os
import pillow_avif
from typing import Union
from bs4 import BeautifulSoup


def catoon_spider(book, vol: Union[int, list], chapter: Union[int, list], author=None, cover=None):
  if isinstance(vol, list):
    start, end = get_start_end(vol)
    for i in list(range(start, end + 1)):
      get_vol_content(book, i, author)
  else:
    get_chapter_content(book, vol, chapter, author)

def get_chapter_content(book, vol: int, chapter: Union[int, list], author=None, cover=None):
  start_chapter, end_chapter = get_start_end(chapter)

  title = f'{book}-第{vol}卷-第{start_chapter}话~第{end_chapter}话'
  
  ebook = create_ebook(title, book, author, cover)

  tocs = []
  chapter_list = []
  for c in list(range(start_chapter, end_chapter+1)):
    ebook = get_ebook_content(ebook, book, vol, c, tocs, chapter_list)
  
  print(f'{book} 爬取完成，保存中。。。')
  # 目录和样式
  ebook.toc = tuple(tocs)
  ebook.spine = ['nav'] + chapter_list
  print(f'bookspine {ebook.spine}')
  ebook.add_item(epub.EpubNcx())
  ebook.add_item(epub.EpubNav())


  # 保存成epub文件
  save_path = os.path.join('.', book, f'{title}.epub')
  epub.write_epub(save_path, ebook)
  print(f'{save_path} 保存成功。')

def get_vol_content(book, vol: int, author=None, cover=None):
  title = f'{book}-第{vol}卷'
  ebook = create_ebook(title, book, author, cover)

  directory_path = rf'.\\catalogs\\葬送的芙莉莲\\第{vol}卷'
  html_files = find_html_files(directory_path)
  tocs = []
  chapter_list = []
  for chapter in html_files:
    ebook = get_ebook_content(ebook, book, vol, chapter, tocs, chapter_list)
  
  print(f'{book} 爬取完成，保存中。。。')
  # 目录和样式
  ebook.toc = tuple(tocs)
  ebook.spine = ['nav'] + chapter_list
  print(f'bookspine {ebook.spine}')
  ebook.add_item(epub.EpubNcx())
  ebook.add_item(epub.EpubNav())


  # 保存成epub文件
  save_path = os.path.join('.', book, title+'.epub')
  epub.write_epub(save_path, ebook)
  print(f'{save_path} 保存成功。')


def get_ebook_content(ebook, book, vol, chapter, tocs, chapter_list):
  '''
  获取指定 卷 话 的漫画ebook内容，并将ebook内容返回。
  注意：须传入tocs与chapter_list，通过浅拷贝，制作漫画目录。
  '''
  i = 0
  html_content = get_html_content(book, vol, chapter)
  # 解析HTML内容
  soup = BeautifulSoup(html_content, 'html.parser')
  catoon_content = soup.find(id="acontentz")  # 找到指定的div
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
    file_name = f"images/image{chapter}_{i}.jpg"
    img_item = epub.EpubItem(uid=f"image{chapter}_{i}", file_name=file_name, media_type="image/jpeg", content=img_data)
    ebook.add_item(img_item)
    img['src'] = file_name
    i = i + 1

  total_content = ''
  for cc in catoon_content.contents:
    if isinstance(cc, str):
      total_content = total_content + cc
    elif cc.name == 'p':
      total_content = total_content + f'<p>{cc.text}</p>'
    elif cc.name == 'img':
      img_content = f'<img class="imagecontent" src="{cc['src']}"/>'
      total_content = total_content + img_content
    elif cc.name == 'br':
      print('br')
      pass
    else:
      print('unknown')
      pass
  
  chapter_name = f'{book} - vol{vol} - chapter{chapter}'
  chapter_html = epub.EpubHtml(title=chapter_name, file_name=f'chapter_{chapter}.xhtml', lang='zh')
  chapter_html.content = f'<html><body><h1>{chapter_name}</h1><div id="TextContent">{total_content}</div></body></html>'
  ebook.add_item(chapter_html)
  tocs.append(epub.Link(f'chapter_{chapter}.xhtml', chapter_name, f'chapter_{chapter}'))
  chapter_list.append(chapter_html)
  return ebook

if __name__=='__main__':
  # # 使用示例
  # directory_path = r'.\\catalogs\\葬送的芙莉莲\\第14卷'  # 替换为你的目录路径
  # html_files = find_html_files(directory_path)
  # for html_file in html_files:
  #   print(html_file)
  catoon_spider('葬送的芙莉莲', 14, [135, 138])