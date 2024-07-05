import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(__file__))
#更改字体
plt.rcParams["font.sans-serif"]=["SimHei"]

GDP_dict = {
    "北京" : 19.00,
    "上海" : 18.04,
    "广州" : 15.36,
    "金华" : 7.8,
    "深圳" : 18.33
}

ECO_dict = {
    "北京" : 7.74,
    "上海" : 7.96,
    "广州" : 7.68,
    "金华" : 5.80,
    "深圳" : 7.27
}

area_mean_dict = {}

# 定义一个函数，用于计算面积均价
def get_area_mean(df):
    # 计算单位面积租金的均价
    area_mean = (df['总价']/df['面积']).mean()

    # 返回一个包含单位面积租金的均价
    return area_mean

# 创建一个空的数据框，用于存储各个城市的统计指标
stats_df = pd.DataFrame()

# 读取每个城市的CSV文件，并调用get_stats函数，将结果添加到stats_df中
for city in ['北京', '上海', '广州', '金华', '深圳']:
    df = pd.read_csv(city + '链家.csv')
    area_mean_dict[city] = get_area_mean(df)
    temp = area_mean_dict[city]
    print(city + "均价为：" + str(temp) + "相对为GDP" + str(temp/GDP_dict[city]) + "倍，相对为人均收入" + str(temp/ECO_dict[city]) + "倍")

#将每个城市的面积均价添加到stats_df中
stats_df['area_mean'] = [stats for city, stats in area_mean_dict.items()]
#将每个城市的GDP和人均收入添加到stats_df中
stats_df['GDP'] = GDP_dict.values() 
stats_df['ECO'] = ECO_dict.values()
#设置stats_df的索引为城市名称
stats_df.index = GDP_dict.keys()
#绘制柱状图，显示每个城市的面积均价，GDP和人均收入
ax = stats_df.plot.bar(rot=0, figsize=(15, 10), title='五个城市的面积均价，GDP和人均收入')
#设置x轴和y轴的标签
ax.set_xlabel('城市') 
ax.set_ylabel('数值')
#显示图形
plt.show()