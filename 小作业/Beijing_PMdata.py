import pandas as pd
import os

os.chdir(os.path.dirname(__file__))

df = pd.read_csv("BeijingPM20100101_20151231.csv")
# 筛选出2015年的数据
df_2015 = df[df["year"] == 2015]
# 保存为新的csv文件
df_2015.to_csv("BeijingPM2015.csv", index=False)
print(df_2015.isnull().sum())

# 读取新的csv文件
df_2015 = pd.read_csv("BeijingPM2015.csv")
# 对PM_xx列使用线性插值法填充缺失值
df_2015["PM_Dongsi"] = df_2015["PM_Dongsi"].interpolate(method="linear")
df_2015["PM_Dongsihuan"] = df_2015["PM_Dongsihuan"].interpolate(method="linear")
df_2015["PM_Nongzhanguan"] = df_2015["PM_Nongzhanguan"].interpolate(method="linear")
df_2015["PM_US Post"] = df_2015["PM_US Post"].interpolate(method="linear")
# 对DEWP和TEMP列使用均值填充缺失值
df_2015["DEWP"] = df_2015["DEWP"].fillna(df_2015["DEWP"].mean())
df_2015["TEMP"] = df_2015["TEMP"].fillna(df_2015["TEMP"].mean())
# 对HUMI、PRES、cbwd和Iws列使用相邻位置的数据填充缺失值
df_2015["HUMI"] = df_2015["HUMI"].fillna(df_2015["PM_Nongzhanguan"])
df_2015["PRES"] = df_2015["PRES"].fillna(df_2015["PM_Nongzhanguan"])
df_2015["cbwd"] = df_2015["cbwd"].fillna(df_2015["PM_Nongzhanguan"])
df_2015["Iws"] = df_2015["Iws"].fillna(df_2015["PM_Nongzhanguan"])
# 对precipitation和Iprec列使用0填充缺失值
df_2015["precipitation"] = df_2015["precipitation"].fillna(0)
df_2015["Iprec"] = df_2015["Iprec"].fillna(0)
# 保存为新的csv文件
df_2015.to_csv("BeijingPM2015_clean.csv", index=False)
print(df_2015.isnull().sum())