import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# 数据准备
N = 1000
x = np.random.randn(N) 
y = np.random.randn(N)

# 用 Matplotlib 画散点图
plt.scatter(x, y,marker='x') 
plt.show()

# 用 Seaborn 画散点图
df = pd.DataFrame({'x': x, 'y': y}) 
sns.jointplot(x="x", y="y", data=df, kind='scatter');
plt.show()

# 数据准备

x = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019] 
y = [5, 3, 6, 20, 17, 16, 19, 30, 32, 35]

# 使用 Matplotlib 画折线图 
plt.plot(x, y) 
plt.show()

# 使用 Seaborn 画折线图 
df = pd.DataFrame({'x': x, 'y': y}) 
sns.lineplot(x="x", y="y", data=df) 
plt.show()

