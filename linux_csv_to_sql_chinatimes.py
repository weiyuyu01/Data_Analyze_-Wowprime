import pandas as pd
import pymysql
from sqlalchemy import create_engine

# 打開 csv 
df = pd.read_csv('chinatimes_220420.csv',sep=",",quotechar='"',header=None,encoding='utf-8')
df.columns = ["來源網站","品牌","發表日期","標題","產業類別","文章內容"]

# table 名稱
table_name = "chinatimes"

# 將 csv 欄位轉 list
web_list = df["來源網站"]
brand_list = df["品牌"]
date_list = df["發表日期"]
title_list = df["標題"]
category_list = df["產業類別"]
content_list = df["文章內容"]

# 無法用 df_tosql 欄位先填 null
null_list = []
for i in range(len(df["品牌"])):
    null_list.append("null")
    
id_list = []
for i in range(1,len(df["品牌"])+1):
    id_list.append(i)

df = pd.DataFrame({
    'id': id_list,
    'web': web_list,
    'brand': brand_list,
    'date': date_list,
    'title': null_list,
    'category': null_list,
    'content': null_list
    })

# 2.將 dataframe 寫入 db
try:
    # MySQL的使用者：root, 密碼:dv101, port：3306, 資料庫：wangsteak
    engine = create_engine('mysql+pymysql://root:dv101@127.0.0.1:3306/wangsteak?charset=utf8')
    # print("資料庫連線成功")
    # if_exists='append' -> 如果表格存在，把資料插入，不存在就創建
    df.to_sql(table_name, engine, if_exists='append', index=False)
    engine.dispose() # 關閉連線
    print("dataframe 寫入成功")
except:
    print("dataframe 寫入失敗")
    
############################################

# 需要分批寫入的欄位
update_list = ["title","category","content"]

# 建立連線
db = pymysql.connect(host="127.0.0.1",user="root", password="dv101",port=3306,database="wangsteak")
print("資料庫連線成功")
cursor = db.cursor() # 建立操作游標，獲得python執行Mysql命令

for list_name in update_list:
    # 1.修改欄位編碼
    try:
        sql = f"ALTER TABLE `{table_name}` CHANGE `{list_name}` `{list_name}` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL;"
        cursor.execute(sql)
        db.commit()
    except pymysql.Error as e:
        db.rollback() # 錯誤則取消修改
        print(f"{list_name} 編碼轉換失敗:"+str(e))

    # 2.內容轉sql語法
    sql_list = [] 
    col_list = locals()[f"{list_name}_list"]
    for i in col_list:
        i = str(i).replace("'","''") # Content 欄位(內容有單引號，寫入db要改成2個單引號)
        sql_list.append(f"{list_name}='{i}'") # 單筆資料格式
        
    # 3.寫入db
    try:
        idx = 0
        for i in sql_list:
            idx += 1
            sql = f"UPDATE `wangsteak`.`{table_name}` SET {i} WHERE id = {idx};"
            cursor.execute(sql)    
        db.commit()
    except pymysql.Error as e:
        db.rollback()
        print(f"{list_name}寫入失敗"+str(e))
        
db.close() # 關閉連線
print(f"{update_list} 欄位寫入成功")

