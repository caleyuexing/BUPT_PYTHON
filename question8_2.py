import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(__file__))
#更改字体
plt.rcParams["font.sans-serif"]=["SimHei"]

# 创建二手房价格字典
area_price_dict = {}

# 读取二手房均价文件
df = pd.read_csv("question8_out.csv", index_col=0)
# 转换为字典
sencond_hand_dict = df.to_dict(orient="index")
# 去掉价格这一层的字典
for city in sencond_hand_dict:
    sencond_hand_dict[city] = sencond_hand_dict[city]["价格"]

# 读取每个城市的CSV文件，并调用get_stats函数，将结果添加到stats_df中
for city in ['北京', '上海', '广州', '深圳', '金华']:
    df = pd.read_csv(city + '链家.csv')
    area_price_dict[city] = df['总价'].mean()/df['面积'].mean()

print("租房面积均价")
print(area_price_dict)
print("二手房面积均价")
print(sencond_hand_dict)

for city in ['北京', '上海', '广州', '深圳', '金华']:
    # 将价格缩小1000倍方便比较
    sencond_hand_dict[city] = sencond_hand_dict[city]/1000

# 创建一个空的数据框，用于存储各个城市的统计指标
stats_df = pd.DataFrame()

#将每个城市的面积均价添加到stats_df中
stats_df['平方米价格'] = sencond_hand_dict.values()
#将每个城市的GDP和人均收入添加到stats_df中
stats_df['面积租金'] = area_price_dict.values() 
#设置stats_df的索引为城市名称
stats_df.index = area_price_dict.keys()
#绘制柱状图，显示每个城市的面积均价，GDP和人均收入
ax = stats_df.plot.bar(rot=0, figsize=(15, 10), title='五个城市的面积租金与缩小1000倍的平方米价格')
#设置x轴和y轴的标签
ax.set_xlabel('城市') 
ax.set_ylabel('数值')
#显示图形
plt.show()