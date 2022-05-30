# Data_Analyze_Wowprime

餐飲趨勢分析
針對王品集團旗下各餐飲品牌聲量、消費者喜好轉換的趨勢等
資料源:找四個論壇、部落格
ex : dcard、ptt、痞客邦等

資料分析步驟：
1. 爬取google map、中時新聞網、facebook等網站上有用資訊,如:評論日期、店家評分、評論內容、按讚數...等,並將所爬取的資訊整理後存成CSV檔。
2. 針對評論/食記內容進行情感分析翰段詞分析,作為一項參考值,並存成新的CSV檔。 
3. 利用python程式,一一將CSV檔讀取並匯入至MYSQL。 
4. 架設API,供使用者存取其指定的集團餐廳的數據內容。

視覺化(Tableau)連結：https://public.tableau.com/app/profile/yichen.lee/viz/_16508197967740/1?publish=yes
