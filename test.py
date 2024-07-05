import pandas as pd
import os

os.chdir(os.path.dirname(__file__))

a = pd.read_csv('test.csv')

a[['几室','other']] = a['房型'].str.split('室|房',expand=True)

print(a)