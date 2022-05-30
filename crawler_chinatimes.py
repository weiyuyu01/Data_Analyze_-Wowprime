import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# 全部品牌請使用 all_keyword_list
all_keyword_list = ['王品集團','王品牛排','西堤','陶板屋','原燒','聚北海道鍋物','藝奇','夏慕尼','品田牧場','石二鍋','HOT 7王品','莆田','青花驕','享鴨','丰禾','12MINI鍋','THE WANG牛排','和牛涮','尬鍋','肉次方']

# 指定的 keyword
keyword = input("請輸入品牌關鍵字：")

# 指定的 keyword 請放入 keyword_list
keyword_list = [keyword] 

page_list = ['1','2','3','4','5','6','7','8','9','10']
final_list = []
for brand_name in keyword_list:
  for page_number in page_list:
    url = 'https://www.chinatimes.com/search/{brand}?page={page}&chdtv'.format(
      brand = brand_name, page=page_number
    )
    #print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    title_soup = soup.find_all('h3',{'class':'title'})
    #print(title_soup)
    # 連結
    for item in title_soup:
      link = item.find('a').get('href')
      try:
        res_content = requests.get(link)
        soup_content = BeautifulSoup(res_content.text,'html.parser')
      except:
        res_content = "null"
      
      # 標題
      try:
        title = soup_content.find('h1',{'class':'article-title'}).text
      except:
        title = "null"
      #print(title)
      # 時間
      try: 
        release_time = soup_content.find('div',{'class':'meta-info'}).find('time').get('datetime')
      except:
        release_time = "null"
      # 產業
      try:
        source = soup_content.find_all('span',{'itemprop':'name'})[1].text
      except:
        source = 'null'
      # 內文
      # 內文存在同一變數
      content_list=[]
      try:
        content_soup = soup_content.find('div',{'class':'article-body'}).find_all('p')
      except:
        content_soup = 'null'
      for item in content_soup:
        try:
          if item.text=='':
            continue
          else:  
            content_list.append(item.text)
        except:
          continue
      final_content = ''.join(content_list)
      
      # 增加"來源網站"欄位
      web_col = "chinatimes"
      
      final_list.append({
        '來源網站':web_col,
        '品牌':brand_name, 
        '發表日期':release_time,
        '標題':title,
        '產業類別':source,
        '文章內容':final_content
      })
      
df = pd.DataFrame(final_list,columns = ["來源網站","品牌","發表日期","標題","產業類別","文章內容"])

date = datetime.now().strftime('%Y%m%d')

# 寫入 csv
with open(f"{date}_chinatimes.csv", mode='a') as f:
    f.write('\n') 
df.to_csv(f"{date}_chinatimes.csv",encoding='utf-8-sig', index=False, mode='a',header=False)
print(f"{date}_chinatimes.csv 寫入完成")

# csv 重新轉碼
df1 = pd.read_csv(f"{date}_chinatimes.csv",sep=",",quotechar='"',header=None,encoding='utf-8')
#df1.columns=["來源網站","品牌","發表日期","標題","產業類別","文章內容"]
df1.to_csv(f"{date}_chinatimes.csv",encoding='utf-8-sig', index=False, mode='w',header=False)