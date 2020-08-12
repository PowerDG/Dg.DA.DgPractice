# -*- coding: utf-8 -*-



import pandas as pd

from pandas import Series, DataFrame
from pandasql import sqldf, load_meat, load_births

x1 = Series([1,2,3,4])

x2 = Series(data=[1,2,3,4], index=['a', 'b', 'c', 'd'])

print(x1,"\n",x2)


data = {'Chinese': [66, 95, 93, 90,80],'English': [65, 85, 92, 88, 90],'Math': [30, 98, 96, 77, 90]}

df1= DataFrame(data)

df2 = DataFrame(data, index=['ZhangFei', 'GuanYu', 'ZhaoYun', 'HuangZhong', 'DianWei'], columns=['English', 'Math', 'Chinese'])

print(df1,"\n",df2)

# score = DataFrame(pd.read_excel('data.xlsx'))

# score.to_excel('data1.xlsx')

# print(score)




df1 = DataFrame({'name':['ZhangFei', 'GuanYu', 'a', 'b', 'c'], 'data1':range(5)})

pysqldf = lambda sql: sqldf(sql, globals())


sql = "select * from df1 where name ='ZhangFei'"

print(pysqldf(sql))

print("-----")
pysqldf = lambda sql: sqldf(sql, globals())

print("======")

