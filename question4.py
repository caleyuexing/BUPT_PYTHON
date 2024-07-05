import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(__file__))

#更改字体
plt.rcParams["font.sans-serif"]=["SimHei"]

# 定义一个函数，用于计算各个区域的均价
def get_mean_price(df):
    # 计算总价(万)列的均值，作为区域的均价
    mean_price = df['总价'].mean()
    mean_area = df['面积'].mean()
    # 返回均价
    return mean_price/mean_area

# 创建一个空的数据框，用于存储各个城市和各个区域的均价
price_df = pd.DataFrame()

cities=['北京', '上海', '广州', '金华', '深圳']

# 读取每个城市的CSV文件，并根据区域进行分组，调用get_mean_price函数，将结果添加到price_df中
for city in cities:
    df = pd.read_csv(city + '链家.csv')
    # 根据区域进行分组
    grouped = df.groupby('区域')
    # 对每个分组，调用get_mean_price函数，得到均价
    for group_name, group_df in grouped:
        mean_price = get_mean_price(group_df)
        # 为均价添加城市和区域列
        price_df = price_df.append({'城市': city, '区域': group_name, '均价': mean_price}, ignore_index=True)

# 设置城市和区域为索引
price_df = price_df.set_index(['城市', '区域'])

# 打印price_df
print(price_df)

# 对每个城市，绘制柱状图，比较各个区域的均价
for city in cities:
    # 选择该城市的数据
    city_df = price_df.loc[city]
    # 绘制柱状图
    city_df.plot(kind='bar', figsize=(10, 6), rot=0)
    plt.xlabel('区域')
    plt.ylabel('均价')
    plt.title(city + '的各个区域的均价')
    plt.show()
