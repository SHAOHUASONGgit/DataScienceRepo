import bs4
import requests
import time

output = open("Houses.json", "w")

for i in range(1,6):

    url = "https://bj.fang.lianjia.com/loupan/pg" + str(i)
    htmldoc = requests.get(url)

    soup = bs4.BeautifulSoup(htmldoc.text,features='html.parser')
    Houses = soup.find_all("div",class_="resblock-desc-wrapper")

    for item in Houses:
        name = item.find("a",class_="name").text
        type = item.find("span",class_="resblock-type").text
        location = item.find("div",class_="resblock-location").find("span").text
        area = item.find("div", class_="resblock-area").find("span").text.replace("建面 ","")
        averageprice = item.find("span",class_="number").text + "元每平方米"
        output.write("楼盘名称：" + name + "  楼盘类型：" + type + "  楼盘街区：" + location + "  楼盘面积：" + area +"  楼盘均价：" + averageprice + "\n")
        print("楼盘名称：" + name + "  楼盘类型：" + type + "  楼盘街区：" + location + "  楼盘面积：" + area +"  楼盘均价：" + averageprice)

    time.sleep(20)

output.close()
