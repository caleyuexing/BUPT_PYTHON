import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(__file__))

#更改字体
plt.rcParams["font.sans-serif"]=["SimHei"]

# 读取每个城市的CSV文件
cities = ['北京', '上海', '广州', '金华', '深圳']
dfs = [pd.read_csv(city + '链家.csv') for city in cities]

# 定义一个函数，用于从朝向列中提取出东南西北四个关键词
def extract_keywords(x):
    keywords = ['东', '南', '西', '北']
    result = []
    for k in keywords:
        if k in x:
            result.append(k)
    return ''.join(result)

# 对每个城市的数据框，根据朝向进行处理，提取出关键词
for df in dfs:
    df['单价'] = df['总价'] / (df['面积'])
    df['关键词'] = df['朝向'].apply(extract_keywords)

# 对每个城市的数据框，按照关键词进行分组，计算单位面积租金的均值
means = [df.groupby('关键词')['单价'].mean() for df in dfs]

# 对每个城市的数据框，将关键词列中的多个关键词拆分成多行
exploded = [df.explode('关键词') for df in dfs]

# 对每个城市，绘制箱线图，比较不同关键词的单位面积租金的分布情况
for city, mean, exp in zip(cities, means, exploded):
    # 绘制箱线图
    print(mean)
    mean.plot(kind='bar', figsize=(10, 6), rot=0)
    plt.xlabel('关键词')
    plt.ylabel('单位面积租金(元/㎡)')
    plt.title(city + '的不同关键词的单位面积租金的分布情况')
    plt.show()

