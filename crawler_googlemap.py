import pandas as pd
import requests 
import json
from datetime import datetime

# 全部品牌 all_keyword_list
# ["王品牛排","西提牛排","陶板屋","原燒","聚北海道鍋物","藝奇","夏慕尼","品田牧場","石二鍋","HOT 7","莆田","青花驕","享鴨","丰禾","12MINI","THE WANG","和牛涮","尬鍋","肉次方"]

# 指定的 keyword
keyword = input("請輸入品牌關鍵字：")

# 指定的 評論頁數 (一頁10篇)
page_num = 10

df = pd.read_csv(f'./google_map_url/google_map_url_{keyword}.csv',sep=",",quotechar='"',header=None,encoding='utf-8')
df.columns=["品牌","分店","地址","api","lat","lng"]

date_list, content_list, star_list, lat_list, lng_list = [],[],[],[],[]
web_col, brand_list ,name_list ,city_list, address_list =[],[],[],[],[]

# 第1～100篇評論，共10個json
page_list = ["1i0","1i10","1i20","1i30","1i40","1i50","1i60","1i70","1i80","1i90"] 
page_list = page_list[:page_num]
 
# 已知欄位複製補齊
for idx in range(len(df["品牌"])):
    for i in range(int(page_num)*10):
        web_col.append("googlemap")
        brand_list.append(df["品牌"][idx])
        name_list.append(df["分店"][idx])
        address_list.append(df["地址"][idx])
        city_list.append(df["地址"][idx][:3])
        lat_list.append(df["lat"][idx])
        lng_list.append(df["lng"][idx])

# 只取每家餐廳所需變換的參數(1y後面數字,2y後面數字)
error_count = 0
for url in df["api"]:
    link_list = url.replace("1y","").replace("2y","").split("!")[2:4]
    a = link_list[0]
    b = link_list[1]
    
    # 每家餐廳要請求10次json
    for i in range(page_num):
        url = f"https://www.google.com/maps/preview/review/listentitiesreviews?authuser=0&hl=zh-TW&gl=tw&pb=!1m2!1y{a}!2y{b}!2m2!{page_list[i]}!2i10!3e1!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1sLCJRYo79OPqUr7wP1uWnuAo!7e81"
        # 發送get請求
        json_text = requests.get(url).text
        # 取代掉特殊字元，這個字元是為了資訊安全而設定
        pretext = ')]}\''
        json_text = json_text.replace(pretext,'')
        # 把字串讀取成json
        soup = json.loads(json_text)
        
        # 取出包含留言的List 。
        conlist = soup[2]
        
        try:
        # 逐筆抓出 (日期(時間戳需轉換)、內容(過濾空格換行)、評分星數)
            for i in conlist:
                dt_object = str(datetime.fromtimestamp(int(str(i[57])[:10]))).split(" ")[0].replace("-","/")
                date_list.append(dt_object) 
                content = (str(i[3])).replace(" ","").replace("\n","") 
                content_list.append(content)
                star_list.append(str(i[4]))
        except:
            error_count += 1
            print(f"留言內容錯誤{error_count}")
            date_list.append("null") 
            content_list.append("null")
            star_list.append("null")

# 寫入 csv
df1 = pd.DataFrame({
    '來源網站': web_col,
    '品牌': brand_list,
    '發表日期': date_list,
    '分店名': name_list,
    '分店地址': address_list,
    '縣市': city_list,
    'lat': lat_list,
    'lng': lng_list,
    '評論內容': content_list,
    '評分星數': star_list
    })

date = datetime.now().strftime('%Y%m%d')

# 寫入 csv
df1.to_csv(f"{date}_googlemap.csv",encoding='utf-8-sig', index=False, mode='a',header=False)

print(f"{date}_googlemap.csv 寫入完成")


