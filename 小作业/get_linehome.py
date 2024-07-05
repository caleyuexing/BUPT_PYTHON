import requests
from bs4 import BeautifulSoup
import csv
import os

os.chdir(os.path.dirname(__file__))

districts = ["dongcheng", "xicheng", "haidian", "chaoyang"]
pages = 5

with open("链家.csv", "w", encoding="gbk") as f:
    writer = csv.writer(f)
    writer.writerow(["楼盘名称", "平米数", "总价", "单价"])

    for district in districts:
        if district == "dongcheng":
            area_name = "东城"
        elif district == "xicheng":
            area_name = "西城"
        elif district == "haidian":
            area_name = "海淀"
        elif district == "chaoyang":
            area_name = "朝阳"
        writer.writerow([area_name])
        for page in range(1, pages + 1):
            url = f"https://bj.lianjia.com/ershoufang/{district}/pg{page}/"
            response = requests.get(url)
            if response.status_code == 200:
                # 解析响应内容，创建BeautifulSoup对象
                soup = BeautifulSoup(response.text, "html.parser")
                # 找到所有的房源信息
                houses = soup.find_all("div", class_="info clear")
                for house in houses:
                    # 提取楼盘名称
                    name = house.find("div", class_="title").a.text
                    # 提取平米数
                    area = house.find("div", class_="address").find("div", class_="houseInfo").text.split("|")[1].strip()
                    # 提取总价
                    total_price = house.find("div", class_="priceInfo").find("div", class_="totalPrice").span.text
                    # 提取单价
                    unit_price = house.find("div", class_="priceInfo").find("div", class_="unitPrice").span.text
                    writer.writerow([name, area, total_price, unit_price])
            else:
                print(f"请求失败，状态码为{response.status_code}")
