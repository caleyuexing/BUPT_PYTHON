import pandas as pd
import requests
from bs4 import BeautifulSoup
import random 
import time
import os

os.chdir(os.path.dirname(__file__))

def ua():
    """随机获取一个浏览器用户信息"""
    
    user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0',
    ]

    agent = random.choice(user_agents)
    
    return {
        'User-Agent': agent
    }


def get(url):
    res = requests.get(url=url, headers = ua())
    return res.text

# 定义一个函数，用于从字符串中提取数字
def extract_number(s):
    # 如果字符串为空，返回None
    if not s:
        return None
    # 否则，去掉所有的非数字字符，包括小数点和逗号
    s = s.replace('.', '').replace(',', '')
    # 尝试将字符串转换为整数，如果失败，返回None
    try:
        return int(s)
    except ValueError:
        return None

# 定义一个函数，用于从面积区间中取中值并取整
def get_area_midpoint(s):
    # 如果字符串为空，返回None
    if not s:
        return None
    # 否则，去掉所有的非数字字符，包括平方米和逗号
    s = s.replace('平方米', '').replace(',', '').replace('㎡', '').replace('建面', '')
    # 尝试将字符串分割为两个数字，如果失败，返回None
    try:
        a, b = map(int, s.split('-'))
    except ValueError:
        return int(float(s))
    # 返回两个数字的平均值并取整
    return round((a + b) / 2)

# 定义一个函数，用于从总价区间中取中值并取整
def get_price_midpoint(s):
    # 如果字符串为空，返回None
    if not s:
        return None
    # 否则，去掉所有的非数字字符，包括万元和逗号
    s = s.replace('元/月', '').replace('总价', '')
    # 尝试将字符串分割为两个数字，如果失败，返回None
    if s.count('-') != 0:
        try:
            a, b = map(int, s.split('-'))
        except ValueError:
            return None
        # 返回两个数字的平均值并取整
        return round((a + b) / 2)
    else:
        return int(float(s))

# 定义一个空列表，用于存储房屋数据
data = []

# 定义一个列表，用于遍历城市
city = ['bj','sh','gz','sz','jh']
# 定义起始网页的url
url = 'https://sh.lianjia.com/zufang/'
pg=1
continueFlag = True 

# 定义一个循环，用于遍历所有的网页
while continueFlag:
    try:
        print(pg)
        pg += 1
        # 发送请求，获取网页内容
        response = get(url)
        # 解析网页内容，使用beautiful soup
        soup = BeautifulSoup(response, 'html.parser')
        # 找到所有的房屋信息的div标签
        divs = soup.find_all('div', class_='content__list--item')
        # 找到当前页面有几个房屋信息
        try:
            house_value = soup.find('span', class_='content__title--hl')
            house_value_num = int(house_value.contents[0])
            if pg > house_value_num/30 + 1 or pg > 2000:
                continueFlag = False
            if house_value_num == 0:
                break
        except:
            continue
        # 遍历每个div标签，提取房屋信息
        for div in divs:
            try:
                # 提取名称，去掉前后空格
                try:
                    name = div.find('a', class_='twoline').text.strip()
                except:
                    continue
                print(name)
                # 提取信息
                category = div.find('p', class_='content__list--item--des').text.strip()
                # 拆解信息
                category = category.replace(' ', '')
                category = category.replace('\n', '')
                try :
                    block1,block2,block3,block4,level = category.split('/')
                    if "仅剩" in block1:
                        continue
                except :
                    continue
                region,block,address = block1.split('-')
                area = block2
                area = get_area_midpoint(area)
                room_type = block4
                # 提取租金，区间取中值并取整
                total_price = div.find('span', class_='content__list--item-price')
                if total_price:
                    total_price = total_price.text.strip()
                else:
                    continue
                total_price = get_price_midpoint(total_price)
                # 将房屋信息以字典的形式添加到列表中
                print("收")
                data.append({
                    '名称': name,
                    '类别': category,
                    '区域': region,
                    '板块': block,
                    '地址': address, 
                    '房型': room_type,
                    '面积': area,
                    '总价': total_price
                })
            except:
                continue
        # 找到下一页的url，如果没有，退出循环
        # 反爬随机停止一段时间
        time.sleep(0.5)
        url = 'https://sh.lianjia.com/zufang/pg' + str(pg) + '/'
        #url = None
    except:
        break


# 将列表转换为数据框
df = pd.DataFrame(data)

# 删除面积缺失的房屋数据
df = df.dropna(subset=['面积'])

# 将数据框保存为csv文件
df.to_csv('上海链家.csv', index=False)