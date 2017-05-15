# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv

# Crawl the website

def crawl(c):
    year=str(c)
    url = "http://dormapply2.adm.nctu.edu.tw/SecondResult/Second" + year + ".html"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml", from_encoding='big5')

# Get Familiar with the data

# print(soup.prettify())

# for row in soup.find_all('tr')[1:3]:
#     for idx, val in enumerate(row.find_all('td')):
#         print(idx, val.text)
#     print("--")

# Iterate through the rows and parse it

    payloads = [["學年度", "階段", "學號", "宿舍", "房號", "是否確認"]]
    for row in (soup.find_all('tr'))[1:1000]:
        room_no = ""
        for idx, val in enumerate(row.find_all('td')):
            if idx==1:
               tmp = val.text.split("樓")
               #val.text 與val.get_text與val的差別
               #為甚麼val[0].text不行
               if val.text=="":
                   dorm = "不明"  
                   room = "不明"            
               else:
                   dorm = tmp[0][:-1]
                   room = tmp[1][:-1]
            if idx==2:
                stu_list = val.text.split("\xa0\xa0\xa0")[:-1]
                for stu in stu_list:
                    s = stu.split("(")
                    if dorm == "不明"  and room == "不明":
                        payload = [year, "不明", s[0], "不明", "不明", "不明"]

                    elif s[1][:-1]==tmp[0]+"樓"+tmp[1] and "(未確認申請)" in stu:
                        payload = [year, "保留原寢", s[0], dorm, room, s[2][:-1]]
               
                    elif s[1][:-1]==tmp[0]+"樓"+tmp[1]:
                        payload = [year, "保留原寢", s[0], dorm, room, ""]
                    elif s[1][:-1]!=tmp[0]+"樓"+tmp[1]:
                        payload = [year, "未保留原寢", s[0], dorm, room, ""]
                    else:
                        payload = [year, "未保留原寢", s[0], dorm, room, s[2][:-1]]
                    payloads.append(payload)
                    print(payload)

# Create csvfile
    with open(year+'.csv', 'w', newline='', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(payloads)
for b in range(98,106):
    crawl(b) 
