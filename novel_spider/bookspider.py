from bs4 import BeautifulSoup
import os
from spiders import catoon_spider

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