import pandas as pd
import os

os.chdir(os.path.dirname(__file__))

# 读取链家.csv文件
beijing = pd.read_csv('北京链家.csv')
shanghai = pd.read_csv('上海链家.csv')
guangzhou = pd.read_csv('广州链家.csv')
shenzhen = pd.read_csv('深圳链家.csv')
jinhua = pd.read_csv('金华链家.csv')

# 将房型变成几室
beijing[['几室','other']] = beijing['房型'].str.split('室|房',expand=True)
shanghai[['几室','other']] = shanghai['房型'].str.split('室|房',expand=True)
guangzhou[['几室','other']] = guangzhou['房型'].str.split('室|房',expand=True)
shenzhen[['几室','other']] = shenzhen['房型'].str.split('室|房',expand=True)
jinhua[['几室','other']] = jinhua['房型'].str.split('室|房',expand=True)

# 只按照几室列分组，计算均价、最高价、最低价、中位数
beijing_stats = beijing.groupby('几室').agg({'总价': ['mean', 'max', 'min', 'median']})
shanghai_stats = shanghai.groupby('几室').agg({'总价': ['mean', 'max', 'min', 'median']})
guangzhou_stats = guangzhou.groupby('几室').agg({'总价': ['mean', 'max', 'min', 'median']})
shenzhen_stats = shenzhen.groupby('几室').agg({'总价': ['mean', 'max', 'min', 'median']})
jinhua_stats = jinhua.groupby('几室').agg({'总价': ['mean', 'max', 'min', 'median']})

# 合并五个城市的统计结果
all_stats = pd.concat([beijing_stats, shanghai_stats, guangzhou_stats, shenzhen_stats, jinhua_stats], axis=1, keys=['北京', '上海', '广州', '深圳', '金华'])


all_stats.to_csv('question3_out.csv', index=False)
print(all_stats)

