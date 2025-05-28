"""
Shohei_Ohtani (大谷翔平)
Yu_Darvish (達比修有)
Gerrit_Cole 
球種:
FF = 四縫線
SL = 滑球
FS = 快速指叉球
CH = 變速
"""


#===載入必要套件===
import os       #os 處理檔案系統（建立資料夾等）
import time     #time 用來設定等待時間
import requests     #requests 發 HTTP 請求（下載影片用）
from bs4 import BeautifulSoup   #BeautifulSoup 解析 HTML
from selenium import webdriver  #selenium 用於自動操作網頁
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



#=== 初始化與設定 ===
#放置影面下載的資料夾名稱，若沒有會自動新增
# output_dir = "Gerrit_Cole_ff_videos"    #Gerrit_Cole FF
# output_dir = "Gerrit_Cole_SL_videos"    #Gerrit_Cole SL
# output_dir = "Gerrit_Cole_CH_videos"    #Gerrit_Cole CH
# output_dir = "Shohei_Ohtani_ff_videos"  #Shohei_Ohtani FF
output_dir = "Shohei_Ohtani_SL_videos"  #Shohei_Ohtani SL
# output_dir = "Shohei_Ohtani_FS_videos"  #Shohei_Ohtani FS
# output_dir = "Yu_Darvish_ff_videos"     #Yu_Darvish FF
# output_dir = "Yu_Darvish_SL_videos"     #Yu_Darvish SL
# output_dir = "Yu_Darvish_FS_videos"     #Yu_Darvish FS
os.makedirs(output_dir, exist_ok=True)

#===設定 Chrome 瀏覽器啟動選項並開啟===
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

# 輸入需要截取的網頁頁面
# search_url = "https://reurl.cc/RY7r86" #Gerrit_Cole FF
# search_url = "https://reurl.cc/DqMyY5" #Gerrit_Cole SL
# search_url = "https://reurl.cc/knb1kr" #Gerrit_Cole CH
# search_url = "https://reurl.cc/RY7rEg" #Shohei_Ohtani FF
search_url = "https://reurl.cc/AMW7zQ" #Shohei_Ohtani SL
# search_url = "https://reurl.cc/M3m0L4" #Shohei_Ohtani FS
# search_url = "https://reurl.cc/6K4Z3O" #Yu_Darvish FF
# search_url = "https://reurl.cc/aebnjZ" #Yu_Darvish SL
# search_url = "https://reurl.cc/nmb1dD" #Yu_Darvish FS
driver.get(search_url)
time.sleep(15)


# 點擊展開指定欄位
try:
    td_to_click = WebDriverWait(driver, 20).until(
        # EC.element_to_be_clickable((By.XPATH, "//*[@id='player_name_543037_']/td[5]")) #Gerrit_Cole
        EC.element_to_be_clickable((By.XPATH, "//*[@id='player_name_660271_']/td[5]")) #Shohei_Ohtani
        # EC.element_to_be_clickable((By.XPATH, "//*[@id='player_name_506433_']/td[5]")) #Yu_Darvish
    )
    td_to_click.click()
    print("✅ 成功點擊展開欄位")
    time.sleep(3)
except Exception as e:
    print(f"❌ 無法點擊展開欄位: {e}")
    driver.quit()
    exit()

# ===自動向下捲動至頁面底部，確保載入全部資料===
# ===不斷捲動網頁直到無新內容為止，用來觸發動態載入===
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

print("📥 開始擷取影片連結...")

# ===抓取影片播放頁面連結===
# 擷取影片連結（第15欄 a[href*='sporty-videos']）
video_links = driver.find_elements(By.XPATH, "//table[contains(@id, 'ajaxTable')]/tbody/tr/td[15]/a[contains(@href, 'sporty-videos?playId=')]")
urls = [link.get_attribute("href") for link in video_links if link.get_attribute("href")][:200] #:抓200筆資料

# === 資料抓取完畢，關閉自動化的 Chrome 瀏覽器===
driver.quit()
print(f"✅ 共擷取 {len(urls)} 筆影片連結，開始下載影片...")

# 影片下載區
for i, url in enumerate(urls):  #對每個影片播放頁面發送 HTTP 請求
    try:
        print(f"[{i+1}/{len(urls)}] 開啟影片頁面: {url}")
        r = requests.get(url)
        if r.status_code != 200:
            print(f"❌ 無法打開影片頁面：{url}")
            continue

        soup = BeautifulSoup(r.text, 'html.parser')     #用 BeautifulSoup 解析影片 HTML 頁面，抓出 <video><source src="..."></source></video> 中的影片網址。
        video_tag = soup.find("video")
        if not video_tag:
            print("❌ 找不到 <video> tag")
            continue
        source = video_tag.find("source")
        if not source or not source.get("src"):
            print("❌ 找不到影片來源")
            continue

        mp4_url = source["src"]
        filename = f"pitch_{i+1:04d}.mp4"   #依照編號命名影片（如 pitch_0001.mp4）
        filepath = os.path.join('train_data',output_dir, filename)

        if os.path.exists(filepath):    #若影片已存在則跳過
            print(f"⏭ 檔案已存在，跳過：{filename}")
            continue

        print(f"⬇️ 正在下載: {mp4_url}")
        with requests.get(mp4_url, stream=True) as vid:     #串流方式下載影片，避免一次將整段影片載入記憶體
            with open(filepath, 'wb') as f:
                for chunk in vid.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✅ 已儲存: {filename}")

    except Exception as e:
        print(f"⚠️ 錯誤：{e}")
