import requests
import bs4

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
}
url = "https://bj.lianjia.com/ershoufang/dongcheng/pg" + "1"
htmldoc = requests.get(url, headers=header)
soup = bs4.BeautifulSoup(htmldoc.text, features='html.parser')
toalInfo = soup.find_all("div", class_="info clear")
for data in toalInfo:
    houseInfo = data.find("div", class_="houseInfo").text.replace(" ", "").split("|")
    houseName = data.find("a", attrs={"data-el": "region"}).text
    houseLayout = houseInfo[0]
    houseArea = float(houseInfo[1].replace("平米", ""))
    houseDirection = houseInfo[2]
    houseLocation = "东城"
    print(houseArea)