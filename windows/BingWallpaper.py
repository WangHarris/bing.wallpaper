import urllib3
import datetime
from PIL import Image
import win32api
import win32con
import win32gui
import re,os


http = urllib3.PoolManager()
url = "https://cn.bing.com/"
save_path = "C:/wallpaper/"
wallpaper_name = datetime.date.today().strftime('%Y-%m-%d') + ".jpeg"


def set_wallpaper_from_bmp(bmp_path):
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmp_path, win32con.SPIF_SENDWININICHANGE)


def set_wallpaper(img_path):
    # 把图片格式统一转换成bmp格式,并放在源图片的同一目录
    img_dir = os.path.dirname(img_path)
    bmpImage = Image.open(img_path)
    new_bmp_path = os.path.join(img_dir, 'wallpaper.bmp')
    bmpImage.save(new_bmp_path, "BMP")
    set_wallpaper_from_bmp(new_bmp_path)


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

set_wallpaper(save_path + wallpaper_name)
