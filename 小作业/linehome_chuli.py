# 导入所需的库
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(__file__))

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

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
        return None
    # 返回两个数字的平均值并取整
    return round((a + b) / 2)

# 定义一个函数，用于从总价区间中取中值并取整
def get_price_midpoint(s):
    # 如果字符串为空，返回None
    if not s:
        return None
    # 否则，去掉所有的非数字字符，包括万元和逗号
    s = s.replace('(万/套)', '').replace('总价', '')
    # 尝试将字符串分割为两个数字，如果失败，返回None
    if s.count('-') != 0:
        try:
            a, b = map(int, s.split('-'))
        except ValueError:
            return None
        # 返回两个数字的平均值并取整
        return round((a + b) / 2)
    else:
        return int(s)

# 定义一个空列表，用于存储房屋数据
data = []

# 定义起始网页的url
url = 'https://bj.fang.lianjia.com/loupan/'
pg=1

# 定义一个循环，用于遍历所有的网页
while url:
    pg += 1
    # 发送请求，获取网页内容
    response = requests.get(url)
    # 解析网页内容，使用beautiful soup
    soup = BeautifulSoup(response.text, 'html.parser')
    # 找到所有的房屋信息的div标签
    divs = soup.find_all('div', class_='resblock-desc-wrapper')
    # 找到当前页面有几个房屋信息
    house_value = soup.find('span', class_='value')
    house_value_num = int(house_value.contents[0])
    if house_value_num == 0:
        break
    # 遍历每个div标签，提取房屋信息
    for div in divs:
        # 提取名称，去掉前后空格
        name = div.find('a', class_='name').text.strip()
        # 提取类别，去掉前后空格
        category = div.find('span', class_='resblock-type').text.strip()
        # 提取地理位置，分别存储区域，板块和地址，去掉前后空格
        location = div.find('div', class_='resblock-location').text.strip()
        location = location.replace('\n/\n', ' ').replace(', ', ',')
        region, block, address = location.split(" ", 2)
        # 提取房型，只保留最小房型，去掉前后空格
        room_type = div.find('a', class_='resblock-room').text.strip()
        room_type = room_type.split('/')[0]
        room_type = room_type.replace('\n', '')
        # 提取面积，区间取中值并取整
        area = div.find('div', class_='resblock-area').text.strip()
        area = get_area_midpoint(area)
        # 提取均价，去掉前后空格
        unit_price = div.find('span', class_='number').text.strip()
        # 提取总价，区间取中值并取整
        total_price = div.find('div', class_='second')
        if total_price:
            total_price = total_price.text.strip()
        else:
            break
        total_price = get_price_midpoint(total_price)
        # 将房屋信息以字典的形式添加到列表中
        data.append({
            '名称': name,
            '类别': category,
            '区域': region,
            '板块': block,
            '地址': address, 
            '房型': room_type,
            '面积': area,
            '均价': unit_price,
            '总价': total_price
        })
    # 找到下一页的url，如果没有，退出循环
    time.sleep(2)
    url = 'https://bj.fang.lianjia.com/loupan/pg' + str(pg) + '/'
    #url = None


# 将列表转换为数据框
df = pd.DataFrame(data)

# 删除面积缺失的房屋数据
df = df.dropna(subset=['面积'])

# 将均价和总价的字符串转换为数字
df['均价'] = df['均价'].apply(extract_number)

# 将数据框保存为csv文件
df.to_csv('lianjia.csv', index=False)

# 数据统计
# 找出总价最贵和最便宜的房子，以及总价的中位数
max_total_price = df['总价'].max()
min_total_price = df['总价'].min()
median_total_price = df['总价'].median()
print(f'总价最贵的房子是：{df[df["总价"] == max_total_price]["名称"].values[0]}，总价为：{max_total_price}万元')
print(f'总价最便宜的房子是：{df[df["总价"] == min_total_price]["名称"].values[0]}，总价为：{min_total_price}万元')
print(f'总价的中位数是：{median_total_price}万元')

# 找出均价最贵和最便宜的房子，以及均价的中位数
max_unit_price = df['均价'].max()
min_unit_price = df['均价'].min()
median_unit_price = df['均价'].median()
print(f'均价最贵的房子是：{df[df["均价"] == max_unit_price]["名称"].values[0]}，均价为：{max_unit_price}元')
print(f'均价最便宜的房子是：{df[df["均价"] == min_unit_price]["名称"].values[0]}，均价为：{min_unit_price}元')
print(f'均价的中位数是：{median_unit_price}元')

# 异常值处理
# 列出总价在均值三倍标准差以外的房屋，展示其基本信息（如果太多可以只展示一部分）
mean_total_price = df['总价'].mean()
std_total_price = df['总价'].std()
outlier_total_price = df[(df['总价'] > mean_total_price + 3 * std_total_price) | (df['总价'] < mean_total_price - 3 * std_total_price)]
print(f'总价在均值三倍标准差以外的房屋有{len(outlier_total_price)}个，它们的基本信息如下：')
print(outlier_total_price)

# 通过箱型图原则判断并列出均价为异常值的房屋，展示其基本信息（如果太多可以只展示一部分）
q1_unit_price = df['均价'].quantile(0.25)
q3_unit_price = df['均价'].quantile(0.75)
iqr_unit_price = q3_unit_price - q1_unit_price
outlier_unit_price = df[(df['均价'] > q3_unit_price + 1.5 * iqr_unit_price) | (df['均价'] < q1_unit_price - 1.5 * iqr_unit_price)]
print(f'均价为异常值的房屋有{len(outlier_unit_price)}个，它们的基本信息如下：')
print(outlier_unit_price)

# 离散化处理
# 对房屋的均价进行离散化处理，自行设定每个区间的长度并给出设置的理由，给出每个区间的房屋数量和所占比例
# 我选择每个区间的长度为5000元，因为这样可以保证区间的数量不会太多或太少，也可以反映均价的分布情况

bins = np.arange(int(df['均价'].min()/5000)*5000, df['均价'].max() + 10000, 5000)
labels = [f'{a}-{b}' for a, b in zip(bins[:-1], bins[1:])]
print(f'区间为：{labels}')
df['均价区间'] = pd.cut(df['均价'], bins=bins, labels=labels, right=False)
counts = df['均价区间'].value_counts(sort=False)
percentages = df['均价区间'].value_counts(normalize=True) * 100

# 将结果保存为csv文件
result = pd.DataFrame({'均价区间': labels, '房屋数量': counts, '所占比例': percentages})
result.to_csv('lianjia_result.csv', index=False)  # 不保存索引列

# 绘制直方图
plt.bar(result['均价区间'], result['房屋数量'])
plt.xticks(rotation=90)  # 旋转x轴刻度标签，以避免重叠
plt.xlabel('均价区间')
plt.ylabel('房屋数量')
plt.title('房屋均价离散图')
plt.show()

# 打印结果
print(result.to_string(index=False))


