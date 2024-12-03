# 导入数据请求模块
import requests
# 导入正则表达式模块
import re
# 导入json模块
import json
# TODO 记得更改你要的url和你自己的cookie
url = 'https://www.bilibili.com/video/BV1234y1F7ZZ/?spm_id_from=333.999.0.0'
cookie = "_uuid=10324EDB8-BC6D-ACA10-7BF2-D51021F95AECF99733infoc; buvid3=6184A61E-F088-DB91-E65D-1BFD0088550998951infoc; b_nut=1714296999; buvid4=03465637-96B3-F0BF-A948-5A494EECA64698951-024042809-JP0MSJrfhvJN7G5Spv3VbkB4016Igw3BlDV3f1Zlpzg%3D; SESSDATA=f6092f37%2C1730001570%2C5dd65%2A42CjCXDGAxL0erDLmV8qAKWkB9uBNYHWeHAOVbtc8Gj1JPzOB-lY7E7pV9-FkyZV5eZewSVjE2X3ZHbHRjek5QZ1BDa3FSeUN1dU9oNWFvUlhGd2lUMFdSeXVKWkRKeldMN3ExTFU2MFFaeGNRMDdHcW1HMGszS0RWTVdMLXVQRGg4UkxVMEJuVS1RIIEC; bili_jct=cddbb22d1e9469a929cf9f72a1ea0d4b; DedeUserID=334717844; DedeUserID__ckMd5=fc36479a3a46f6aa; enable_web_push=DISABLE; header_theme_version=CLOSE; home_feed_column=5; CURRENT_FNVAL=4048; rpdid=0z9Zw2XKKu|5kY1LGIo|5ue|3w1S1OVF; PVID=1; CURRENT_QUALITY=116; buvid_fp_plain=undefined; fingerprint=8e98d5c44bba37fa89c535e13034ecae; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjEyODg4ODksImlhdCI6MTcyMTAyOTYyOSwicGx0IjotMX0.kdk_6aR6FCRJXbv1H0FK3T1M5ow-g0Cj8Do4zH7dGDs; bili_ticket_expires=1721288829; b_lsid=98D273BF_190B5659D65; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com; sid=8rfuf63c; browser_resolution=1699-944; buvid_fp=1adad01b8b82fa1ed31de5a6ce9752ed; VIP_CONTENT_REMIND=1; bp_t_offset_334717844=954320284104523776"
headers = {
        # Referer 防盗链 告诉服务器你请求链接是从哪里跳转过来的
        # "Referer": "https://www.bilibili.com/video/BV1454y187Er/",
        "Referer": url,
        # User-Agent 用户代理, 表示浏览器/设备基本身份信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Cookie": cookie
}
# 发送请求
response = requests.get(url=url, headers=headers)
html = response.text
print(html)
# 解析数据: 提取视频标题
title = re.findall('title="(.*?)"', html)[0]
print(title)
# 提取视频信息
info = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
# info -> json字符串转成json字典
json_data = json.loads(info)
# 提取视频链接
video_url = json_data['data']['dash']['video'][0]['base_url']
print(video_url)
# 提取音频链接
audio_url = json_data['data']['dash']['audio'][0]['base_url']
print(audio_url)


print('get audio content...')
audio_content = requests.get(url=audio_url, headers=headers).content

print('get video content...')
video_content = requests.get(url=video_url, headers=headers).content

# 保存数据
with open('video\\' + title + '.mp4', mode='wb') as v:
    v.write(video_content)
with open('video\\' + title + '.mp3', mode='wb') as a:
    a.write(audio_content)



from moviepy.editor import VideoFileClip, AudioFileClip

# 加载视频文件
video = VideoFileClip('video\\' + title + '.mp4')

# 加载音频文件
audio = AudioFileClip('video\\' + title + '.mp3')

# 将音频添加到视频中
video_with_audio = video.set_audio(audio)

# 导出带音频的视频
video_with_audio.write_videofile('video\\' + title + '_merge.mp4', codec="libx264", audio_codec="aac")
