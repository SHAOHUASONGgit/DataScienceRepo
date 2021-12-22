import bs4
import requests
import time

output = open("Houses.json", "w", encoding='utf-8')
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
}
for i in range(1,19):
    url = "https://bj.fang.lianjia.com/loupan/pg" + str(i)#翻页
    htmldoc = requests.get(url, headers=header)
    soup = bs4.BeautifulSoup(htmldoc.text, features='html.parser')
    Houses = soup.find_all("div", class_="resblock-desc-wrapper")
    for item in Houses:
        name = item.find("a", class_="name").text.replace(" ", "-")
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
