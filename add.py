import pandas as pd # 数据存储
import os

os.chdir(os.path.dirname(__file__))

city = ["北京", "上海", "广州", "深圳", "金华"]

for i in city:
    # 读取IRIS.csv数据集
    a = pd.read_csv( i + "链家.csv")
    # 使用正则表达式从B列提取朝向信息并保存到新列'Direction'
    a['朝向'] = a['类别'].str.extract('/[^/]*/([^/]*)/')
    # 保存到新的CSV文件
    a.to_csv(i + "链家.csv", index=False)
