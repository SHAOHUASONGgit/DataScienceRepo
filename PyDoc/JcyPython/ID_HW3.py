import csv
import calendar

input = open("pm25-data-for-five-chinese-cities/BeijingPM20100101_20151231.csv","r")
reader = csv.reader(input)

year_month = []
DongsiMonthAverage = []
DongsihuanMonthAverage = []
NongzhanguanMonthAverage = []
USMonthAverage = []

tagline = reader.__next__()
for line in reader:

    year = line[1]
    month = line[2]
    days = calendar.monthrange(int(year) , int(month))[1]
    DongsiPM = (float(line[6]) if line[6] != "NA" else float(0))
    DongsihuanPM = (float(line[7]) if line[7] != "NA" else float(0))
    NongzhanguanPM = (float(line[8]) if line[8] != "NA" else float(0))
    USPM = (float(line[9]) if line[9] != "NA" else float(0))

    if ((str(year) + "_" +str(month)) not in year_month):
        year_month.append((str(year) + "_" +str(month)))
        average_tag = len(year_month) - 1
        DongsiMonthAverage.append(float(0))
        DongsihuanMonthAverage.append(float(0))
        NongzhanguanMonthAverage.append(float(0))
        USMonthAverage.append(float(0))
    else:
        DongsiMonthAverage[average_tag] += (DongsiPM) / 24 / days
        DongsihuanMonthAverage[average_tag] += (DongsihuanPM) / 24 / days
        NongzhanguanMonthAverage[average_tag] += (NongzhanguanPM) / 24 / days
        USMonthAverage[average_tag] += (USPM) / 24 / days

        DongsiMonthAverage[average_tag] = round(DongsiMonthAverage[average_tag] , 2)
        DongsihuanMonthAverage[average_tag] = round(DongsihuanMonthAverage[average_tag], 2)
        NongzhanguanMonthAverage[average_tag] = round(NongzhanguanMonthAverage[average_tag], 2)
        USMonthAverage[average_tag] = round(USMonthAverage[average_tag], 2)

input.close()

years = int(len(year_month) / 12)
DongsiYearAverage = []
DongsihuanYearAverage = []
NongzhanguanYearAverage = []
USYearAverage = []
Year = []

for i in range(years):
    Year.append(year_month[i*12][0:4])
    DongsiYearAverage.append(round(sum(DongsiMonthAverage[i * 12 : (i+1) * 12]) / 12 , 2))
    DongsihuanYearAverage.append(round(sum(DongsihuanMonthAverage[i * 12 : (i+1) * 12]) / 12 , 2))
    NongzhanguanYearAverage.append(round(sum(NongzhanguanMonthAverage[i * 12 : (i+1) * 12]) / 12 , 2))
    USYearAverage.append(round(sum(USMonthAverage[i * 12 : (i+1) * 12]) / 12 , 2))

year_month.insert(0,"年_月")
DongsiMonthAverage.insert(0,"Dongsi月均值")
DongsihuanMonthAverage.insert(0,"Dongsihuan月均值")
NongzhanguanMonthAverage.insert(0,"Nongzhanguan月均值")
USMonthAverage.insert(0,"US月均值")

Year.insert(0,"年")
DongsiYearAverage.insert(0,"Dongsi年均值")
DongsihuanYearAverage.insert(0,"Dongsihuan年均值")
NongzhanguanYearAverage.insert(0,"Nongzhanguan年均值")
USYearAverage.insert(0,"US年均值")

output = open("PM_BeiJing.csv","w")
writer = csv.writer(output)

writer.writerow(year_month)
writer.writerow(DongsiMonthAverage)
writer.writerow(DongsihuanMonthAverage)
writer.writerow(NongzhanguanMonthAverage)
writer.writerow(USMonthAverage)

writer.writerow(["-"] * len(year_month))

writer.writerow(Year)
writer.writerow(DongsiYearAverage)
writer.writerow(DongsihuanYearAverage)
writer.writerow(NongzhanguanYearAverage)
writer.writerow(USYearAverage)

output.close()