import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(__file__))

#更改字体
plt.rcParams["font.sans-serif"]=["SimHei"]

# 定义一个函数，用于计算各种统计指标
def get_stats(df):
    # 计算租金的均价、最高价、最低价、中位数
    rent_mean = df['总价'].mean()
    rent_max = df['总价'].max()
    rent_min = df['总价'].min()
    rent_median = df['总价'].median()

    # 计算单位面积租金的均价、最高价、最低价、中位数
    area_mean = (df['总价']/df['面积']).mean()
    area_max = (df['总价']/df['面积']).max()
    area_min = (df['总价']/df['面积']).min()
    area_median = (df['总价']/df['面积']).median()

    # 返回一个包含所有指标的字典
    return {'rent_mean': rent_mean, 'rent_max': rent_max, 'rent_min': rent_min, 'rent_median': rent_median,
            'area_mean': area_mean, 'area_max': area_max, 'area_min': area_min, 'area_median': area_median}

# 创建一个空的数据框，用于存储各个城市的统计指标
stats_df = pd.DataFrame()

# 读取每个城市的CSV文件，并调用get_stats函数，将结果添加到stats_df中
for city in ['北京', '上海', '广州', '金华', '深圳']:
    df = pd.read_csv(city + '链家.csv')
    stats = get_stats(df)
    stats_df = stats_df.append(stats, ignore_index=True)

# 为stats_df添加城市列
stats_df['城市'] = ['北京', '上海', '广州', '金华', '深圳']

# 设置城市列为索引
stats_df = stats_df.set_index('城市')

# 打印stats_df
print(stats_df)

# 绘制柱状图，比较各个城市的租金均价
plt.figure() # 增加这一行，创建一个新的图形
stats_df['rent_mean'].plot(kind='barh', figsize=(10, 6), rot=0) 
plt.xlabel('租金均价(万)')
plt.ylabel('城市')
plt.title('各个城市的租金均价')
plt.show()

# 绘制柱状图，比较各个城市的单位面积租金均价
plt.figure() # 增加这一行，创建一个新的图形
stats_df['area_mean'].plot(kind='barh', figsize=(10, 6), rot=0) 
plt.xlabel('单位面积租金均价(元/㎡)')
plt.ylabel('城市')
plt.title('各个城市的单位面积租金均价')
plt.show()
