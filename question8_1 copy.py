import pandas as pd
import os

os.chdir(os.path.dirname(__file__))

citys = ['北京','上海','广州','深圳','金华']
citys_2 = {'北京' : 54171,
         '上海' : 60527,
         '广州' : 36633,
         '深圳' : 63862,
         '金华' : 16833}

area_price_dict = {}

for city in citys:
    area_price_dict[city] = citys_2[city]

print(area_price_dict)
result = pd.DataFrame.from_dict(area_price_dict, orient='index', columns=['价格'])
# 将数据框保存为csv文件
result.to_csv('question8_out.csv')