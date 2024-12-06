import requests
import os
from typing import Union
from pathlib import Path
from ebooklib import epub

def get_html_content(book: str, vol: Union[str, int], chapter: Union[str, int], prefix='catalogs'):
    if isinstance(vol, int):
        vol = f'第{vol}卷'
    if isinstance(chapter, int):
        chapter = f'第{chapter}话.html'
        
    # 指定文件路径
    file_path = os.path.join(prefix, book, vol, chapter)
    print(file_path)

    try:
        # 打开文件
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取整个文件内容
            content = file.read()
            # print(content)
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到，请检查路径是否正确。")
    except IOError:
        print(f"发生I/O错误，无法读取文件 {file_path}。")

    return content

def get_img(url):
  # url = 'https://img3.readpai.com/0/41/117273/231236.jpg'

  headers = {
    "authority": "i.motiezw.com",
    "method": "GET",
    "path": "/0/1/2/30.jpg",
    "scheme": "https",
    "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "i",
    "referer": "https://www.bilimanga.net/",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
  }

  response = requests.get(url, headers=headers)
  img_data = response.content
  # if url.endswith('.avif'):
  #   img_filename = 'image.avif'
  #   # 保存图片到本地
  #   with open(img_filename, 'wb') as img_file:
  #       img_file.write(img_data)
  print("download over")
  
  return img_data

def find_html_files(directory):
  # 创建一个Path对象
  path = Path(directory)
  html_files = [p.name for p in path.rglob("*.html")]
  return html_files

def get_start_end(x: Union[int, list]):
    start = end = 0
    if isinstance(x, int):
        start = end = x
    elif(x, list):
        start = x[0]
        end = x[1]
    return start, end

author_dict = {
    '葬送的芙莉莲': '山田鐘人'
}

def create_ebook(title, book='unknown', author = None, cover = None):
    # 创建电子书
    ebook = epub.EpubBook()
    ebook.set_title(title)
    ebook.set_language('zh')

    if not author:
        author = author_dict.get(book, '佚名')
    ebook.add_author(author)

    if not cover == None:
        book_cover = get_img(cover)
        ebook.set_cover(f'{title}.jpg', book_cover)
    
    return ebook