import bs4
import requests
import time

output = open("Houses.json", "w", encoding='utf-8')
for i in range(1,19):
    url = "https://bj.fang.lianjia.com/loupan/pg" + str(i)#翻页
    htmldoc = requests.get(url)
    soup = bs4.BeautifulSoup(htmldoc.text,features='html.parser')
    Houses = soup.find_all("div",class_="resblock-desc-wrapper")
    for item in Houses:
        name = item.find("a",class_="name").text
        averageprice = item.find("span", class_="number").text
        if averageprice == "":
            averageprice = str(0)
        averageprice += "元/m2"
        area = item.find("div", class_="resblock-area").find("span").text.replace("建面 ", "").replace("㎡", "")
        if area == "":
            area = str(0)
        area += "m2"
        region = item.find("div", class_="resblock-location").find("span").text
        output.write(name+", "+region+", "+averageprice+", "+area+"\n")
    time.sleep(10)#休眠以免封ip
output.close()
