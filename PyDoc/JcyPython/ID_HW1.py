import bs4
import requests

url = "https://v1-www.xuetangx.com/partners"
htmldoc = requests.get(url)

soup = bs4.BeautifulSoup(htmldoc.text,features='html.parser')
SchoolAndCourse = soup.find_all("div",class_="text_con")

output = open("SchoolAndCourse.json", "w")

for item in SchoolAndCourse:
    School = item.find("h3").text
    Course = item.find("p").text.replace("门课程",'')
    output.write(School + "," + Course + "\n")

output.close()
