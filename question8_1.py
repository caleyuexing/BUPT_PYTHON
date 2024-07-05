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

# 定义一个函数，用于从总价区间中取中值并取整
def get_price_midpoint(s):
    # 如果字符串为空，返回None
    if not s:
        return None
    # 否则，去掉所有的非数字字符，包括万元和逗号
    s = s.replace('元/平', '').replace(',', '')
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
citys = ['bj','sh','gz','sz','jh']

area_price_dict = {}

pg=1
continueFlag = True 
for city in citys:
    # 定义起始网页的url
    url = 'https://' + city + '.lianjia.com/ershoufang/pg' + str(pg) + '/'
    # 定义一个循环，用于遍历所有的网页
    while continueFlag:

        print(pg)
        pg += 1
        # 发送请求，获取网页内容
        response = get(url)
        # 解析网页内容，使用beautiful soup
        soup = BeautifulSoup(response, 'html.parser')
        # 找到所有的房屋信息的div标签
        divs = soup.find_all('div', class_='clear LOGCLICKDATA')
        # 遍历每个div标签，提取房屋信息
        for div in divs:
            # 提取面积均价
            price = div.find('div', class_='unitPrice').text.strip()
            if price:
                price = price.text.strip()
            else:
                continue
            price = get_price_midpoint(price)
            print(price)
            # 将房屋信息以字典的形式添加到列表中
            data.append({
                '面积均价': price
            })
        # 找到下一页的url，如果没有，退出循环
        # 反爬随机停止一段时间
        time.sleep(0.5)
        url = 'https://'+ city +'.lianjia.com/ershoufang/pg' + str(pg) + '/'
        #url = None


    # 将列表转换为数据框
    df = pd.DataFrame(data)
    price_mean = df['面积均价'].mean()
    if city == 'bj':
        city_ch = '北京'
    elif city == 'sh':
        city_ch = '上海'
    elif city == 'gz':
        city_ch = '广州'
    elif city == 'sz':
        city_ch = '深圳'
    else:
        city_ch = '金华'

    area_price_dict[city_ch] = price_mean

result = pd.DataFrame.from_dict(area_price_dict, orient='index', columns=['价格'])
# 将数据框保存为csv文件
result.to_csv('question8_out.csv')