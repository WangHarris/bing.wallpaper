import urllib3
import re
import datetime
import os


http = urllib3.PoolManager()
url = "https://cn.bing.com/"
save_path = "/home/harris/Pictures/MyImageHosting/img/wallpaper/"
wallpaper_name = datetime.date.today().strftime('%Y-%m-%d') + ".jpeg"


def download(url, num_retries=2):
    print("Downloading: ", url)
    response = http.request("GET", url)
    if 500 <= response.status < 600 and num_retries > 0:
        return download(url, num_retries-1)
    return response.data


html = download(url).decode('utf-8')
wallpaper_src = url + re.findall('data-ultra-definition-src="(.*?)"', html)[0]

if not os.path.exists(save_path):
    os.mkdir(save_path)

with open(save_path+wallpaper_name, "wb") as f:
    f.write(download(wallpaper_src))

os.system('gsettings set org.gnome.desktop.background picture-uri "file:{file_full_name}"'.format(file_full_name=save_path+wallpaper_name))
