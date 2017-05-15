import requests
from bs4 import BeautifulSoup
import csv

    
def crawl(c):
    year=str(c)
    url = "http://dormapply2.adm.nctu.edu.tw/ThirdResult/ThirdUB"+year+".html"
    r=requests.get(url)
    soup = BeautifulSoup(r.content,"lxml",from_encoding="big5")

    payloads = [["學年度", "階段", "學號", "宿舍", "房號"]]
    for row in (soup.find_all('tr'))[1:1000]:
        for idx, val in enumerate(row.find_all('td')):
            if idx==1:
                stu_list=val.text.split(",")
            if idx==2:
                sel=val.text.split("(")
            if idx==4:
                tmp=val.text.split("室")
                room=tmp[0][-3:]
                #102年不能用切樓出來
                home=val.text.split("(")
                dorm=home[1][0:3]
            
                for stu in stu_list[:-1]:
                    if dorm==sel[0][0:3]:
                        payload = [year, "第一志願", stu, dorm, room]
    
                    elif dorm==sel[1][2:5]:
                        payload = [year, "第二志願", stu, dorm, room]
    
                    elif dorm==sel[2][2:5]:
                        payload = [year, "第三志願", stu, dorm, room]

                    else:
                        payload = [year, "第四志願", stu, dorm, room]

                    payloads.append(payload)
                    print(payload)
            
    with open(year+'third.csv', 'w', newline='', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(payloads)

for b in range(98,99):
    crawl(b)


