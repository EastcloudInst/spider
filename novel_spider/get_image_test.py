import requests
from bs4 import BeautifulSoup

def get_img(url):
  # url = 'https://img3.readpai.com/0/41/117273/231236.jpg'

  headers = {
    "authority": "img3.readpai.com",
    "method": "GET",
    "scheme": "https",
    "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6",
    "priority": "u=2, i",
    "referer": "https://www.linovelib.com/",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
  }

  headers2 = {
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

  response = requests.get(url, headers=headers2)
  img_data = response.content
  # if url.endswith('.avif'):
  #   img_filename = 'image.avif'
  #   # 保存图片到本地
  #   with open(img_filename, 'wb') as img_file:
  #       img_file.write(img_data)
  print("download over")
  
  return img_data


get_img('https://i.motiezw.com/0/1/2/1.jpg')
