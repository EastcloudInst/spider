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

  response = requests.get(url, headers=headers)
  img_data = response.content
  # img_filename = 'image.jpg'
  # # 保存图片到本地
  # with open(img_filename, 'wb') as img_file:
  #     img_file.write(img_data)
  print("download over")
  
  return img_data

# # 原始HTML内容
# html_content = '''
# <p>「唔喔喔喔喔喔喔喔！」</p>
# <p>所以我朝着下坡，使劲踏起脚踏车的踏板……</p>
# <p>「喔喔喔……停停停停停，哟咻。」</p>
# <p>重新考虑过以后，下了脚踏车的我将脚架细心地立好……</p>
# <p>「再次出发唔喔喔喔喔喔喔喔喔喔～～！」</p>
# <br>
# <img src="https://img3.readpai.com/0/41/117273/231235.jpg" class="imagecontent">
# <br>
# <p>我改两条腿全力冲下去。</p>
# <p>这做会让速度和帅气度下滑，不过没办法。</p>
# <p>因为，这才是符合这个国家通规则的正当追赶方式。</p>
# <p>尽管全力冲刺也很危险，但腿赶路大概就不会被视为违规了。</p>
# <p>弱势行人万岁。</p>
# <br>
# <p>※ ※ ※</p>
# <br>
# <p>当晚……</p>
# <p>过了十二点，跟往常一，来录动画的两台硬碟式录放影机正发出低鸣声运，不输给机器废热的键盘热情敲打声也在房间里响着。</p>
# <br>
# <p>标题：</p>
# '''

# # 本地图片路径
# local_image_path = "images/local_image.jpg"

# # 解析HTML内容
# soup = BeautifulSoup(html_content, 'html.parser')

# # 查找所有的img标签
# images = soup.find_all('img')

# # 替换img标签中的src属性值
# for img in images:
#     img['src'] = local_image_path

# # 输出修改后的HTML内容
# modified_html = str(soup)
# print(modified_html)
