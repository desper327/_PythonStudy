# -*- coding:utf-8 -*-
import os
import requests
import random
input_name = input("请输入你要下载的歌曲ID：")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1651235981; _ga=GA1.2.593351211.1651235981; _gid=GA1.2.1236513393.1651235981; _gat=1; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1651236048; kw_token=44Y6M2EQ515',
    'csrf': '44Y6M2EQ515',
    'Host': 'www.kuwo.cn',
    'Referer': 'http://www.kuwo.cn/search/list?key=%E5%AD%A4%E5%8B%87%E8%80%85'
}

music_url = f'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={input_name}&type=convert_url3&br=320kmp3'

download_url = requests.get(music_url).json()["data"]["url"]
music = requests.get(download_url).content
if not os.path.exists(r"./music"):
    os.mkdir(r"./music")
else:
    aaa = random.randint(1,1000)
    with open(f'./{aaa}.mp3', mode="wb") as f:
        f.write(music)
        print(f"下载成功，你的歌曲在本地被命名为：{aaa}.mp3")