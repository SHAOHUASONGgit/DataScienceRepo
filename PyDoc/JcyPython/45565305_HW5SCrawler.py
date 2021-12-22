import csv

import requests
import bs4
import time

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
}
totalLocation = {"东城": "dongcheng", "西城": "xicheng", "朝阳": "chaoyang", "海淀": "haidian"}
output = open("lianjia.csv", "w", encoding='utf-8-sig', newline='')
writer = csv.writer(output)
writer.writerow(["片区", "总价(万元)", "小区", "朝向", "面积"])
for location in list(totalLocation.keys()):
    for pages in range(1,11):
        url = "https://bj.lianjia.com/ershoufang/" + str(totalLocation.get(location)) + "/pg" + str(pages)
        htmldoc = requests.get(url, headers=header)
        soup = bs4.BeautifulSoup(htmldoc.text, features='html.parser')
        toalInfo = soup.find_all("div", class_="info clear")
        for data in toalInfo:
            houseInfo = data.find("div", class_="houseInfo").text.replace(" ", "").split("|")
            housePrice = data.find("div", class_="totalPrice totalPrice2").find("span").text
            houseName = data.find("a", attrs={"data-el": "region"}).text.replace(" ", "")
            houseLayout = houseInfo[0]
            houseArea = float(houseInfo[1].replace("平米", ""))
            houseDirection = houseInfo[2]
            csvInfo = [location, housePrice, houseName, houseLayout, str(houseArea)]
            writer.writerow(csvInfo)
        time.sleep(5)
    print(location + " Done!")
output.close()