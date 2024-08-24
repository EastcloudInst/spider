# TODO 视频网址
url = 'https://www.bilibili.com/bangumi/play/ss45303?theme=movie&spm_id_from=333.337.0.0'
headers = {
        # Referer 防盗链 告诉服务器你请求链接是从哪里跳转过来的
        # "Referer": "https://www.bilibili.com/video/BV1454y187Er/",
        "Referer": url,
        # User-Agent 用户代理, 表示浏览器/设备基本身份信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }
import requests
# TODO 通过F12查看视频的地址
video_url = 'https://upos-sz-mirror08c.bilivideo.com/upgcxcode/80/48/1180244880/1180244880-1-100143.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=\u0026uipk=5\u0026nbs=1\u0026deadline=1721039386\u0026gen=playurlv2\u0026os=08cbv\u0026oi=0\u0026trid=a2acf48626f84fa6b0d35ffa6b6c10e1p\u0026mid=334717844\u0026platform=pc\u0026og=hw\u0026upsig=f946fe6e121d845f55755574052a897d\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\u0026bvc=vod\u0026nettype=0\u0026orderid=0,3\u0026buvid=6184A61E-F088-DB91-E65D-1BFD0088550998951infoc\u0026build=0\u0026f=p_0_0\u0026agrr=1\u0026bw=95186\u0026logo=80000000'

video_response = requests.get(video_url, headers=headers)
with open('shiping.mp4', mode='wb') as v:
    v.write(video_response.content)
    
# TODO 通过F12查看音频的地址
audio_url = 'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/80/48/1180244880/1180244880-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=\u0026uipk=5\u0026nbs=1\u0026deadline=1721039386\u0026gen=playurlv2\u0026os=cosbv\u0026oi=0\u0026trid=a2acf48626f84fa6b0d35ffa6b6c10e1p\u0026mid=334717844\u0026platform=pc\u0026og=cos\u0026upsig=217a5ac9415b927fb979d40e52bb5c2b\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\u0026bvc=vod\u0026nettype=0\u0026orderid=0,3\u0026buvid=6184A61E-F088-DB91-E65D-1BFD0088550998951infoc\u0026build=0\u0026f=p_0_0\u0026agrr=1\u0026bw=24045\u0026logo=80000000'
audio_response = requests.get(audio_url, headers=headers)
with open('yingping.mp3', mode='wb') as v:
    v.write(audio_response.content)
