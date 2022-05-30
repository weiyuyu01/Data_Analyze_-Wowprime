from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from datetime import datetime

UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless") # 隱藏瀏覽器畫面
chrome_options.add_argument("--no-sandbox") # 以最高權限運行
chrome_options.add_argument("user-agent=" + UserAgent)
driver = webdriver.Chrome(options=chrome_options)

# 全部品牌 all_keyword_list
# ["王品牛排","西提牛排","陶板屋","原燒","聚北海道鍋物","藝奇","夏慕尼","品田牧場","石二鍋","HOT 7","莆田","青花驕","享鴨","丰禾","12MINI","THE WANG","和牛涮","尬鍋","肉次方"]

# 指定的 keyword
keyword = input("請輸入品牌關鍵字：")

url = f"https://www.pixnet.net/tags/{keyword}?filter=articles&sort=latest"
driver.get(url)
time.sleep(2)
# 一直往下滑動
x = 0
while True:
    x += 1
    js="window.scrollTo(0,document.body.scrollHeight)"
    # jsCode = "window.scrollBy(0,-500)"
    driver.execute_script(js)
    time.sleep(1)
    jsCode1 = "window.scrollBy(0,-500)"
    driver.execute_script(jsCode1)
    time.sleep(1)
    if x > 30 : break # 設定上限，30是100篇
    try:
# 抓取到footer的標籤就停止
        content = driver.find_element(By.CLASS_NAME, 'bWmKqq')
        print(content.text) # bWmKqq ---> 沒有更多相關結果了～
        break
    except:
        pass

while True:
    # 取得文章連結網址 link_list
    elems = driver.find_elements(By.CLASS_NAME, "sc-1d5amb4-1")
    link_list = [elem.get_attribute('href') for elem in elems]
    print(f"{keyword}文章連結筆數",len(link_list))

    # 取得文章標題 title_list
    title = driver.find_elements(By.CLASS_NAME, "sc-1d5amb4-0")
    title_list = [i.text for i in title]

    # 取得文章日期 date_list
    date = driver.find_elements(By.CLASS_NAME, "sc-15yfh73-8")
    date_list = []
    # 當年度文章沒有年，要補回去
    year = time.strftime('%Y', time.localtime())
    for i in date:
        i = i.text
        if "年" not in i : i = (f"{year}年"+ i)
        i = i.split(" ")[0].replace("年","/").replace("月","/").replace("日","")
        date_list.append(i)
    
    if len(link_list) == 0 : 
        print("連線發生錯誤，準備重試!")
        time.sleep(3)
    else:
        break


# 迴圈遍歷網址，進入每篇文章取得內文、留言數、觀看數
content_list, msg_count, view_count = [],[],[]
def get_content(link_list):
    count = 0 # 文章計數
    for i in link_list:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(i)
        time.sleep(1)
        
        # 取得文章內容 content 存入 content_list
        try:
            content = driver.find_element(By.CLASS_NAME, "article-content-inner").text.replace(" ","").replace("\n","")
            content_list.append(content)
        except:
            # 文章無法取得則寫入 null 
            content_list.append("null")
            count += 1
            pass
        try:
            # 留言數 msg_count, 觀看數 view_count
            num = driver.find_element(By.CLASS_NAME, "author").text
            new_num = num.split("留言")[1].split(" 人氣")
            msg = new_num[0].replace("(","").replace(")","")
            view = new_num[1].replace("(","").replace(")","")
            if msg.isdigit() and view.isdigit() == True :
                msg_count.append(int(msg))
                view_count.append(int(view))
            else: print(int("except"))
        except:    
            msg_count.append(0)  
            view_count.append(0)

    return content_list, msg_count, view_count

get_content(link_list)

# 增加"來源網站"欄位
web_col = ["pixnet" for i in range(len(date_list))]
# 增加欄位 品牌、文章内容(先填null值)
brand_col = [keyword for i in range(len(date_list))]

# 寫入 csv
df = pd.DataFrame({
    '來源網站': web_col,
    '品牌': brand_col,
    '發表日期': date_list,
    '標題': title_list,
    '文章內容': content_list,
    '瀏覽數': view_count,
    '留言數': msg_count
    })

date = datetime.now().strftime('%Y%m%d')

# 寫入 csv
df.to_csv(f"{date}_pixnet.csv",encoding='utf-8-sig', index=False, mode='a',header=False)


print(f"{date}_pixnet.csv 寫入完成")
