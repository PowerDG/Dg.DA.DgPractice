# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 21:19:38 2019

@author: PowerDg
"""
import numpy as np

name = input("What's your name?")

sum = 100+100

print ('hello,%s' %name)

print ('sum = %d' %sum)

sum = 0

for number in range(11):

    sum = sum + number

print(sum)

import numpy as np

a = np.array([1, 2, 3])

b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

b[1,1]=10

print(a,a.shape,a.dtype,"\n", b,b.shape,b.dtype)

persontype = np.dtype({

    'names':['name', 'age', 'chinese', 'math', 'english'],

    'formats':['S32','i', 'i', 'i', 'f']})

peoples = np.array([("ZhangFei",32,75,100, 90),("GuanYu",24,85,96,88.5),

       ("ZhaoYun",28,85,92,96.5),("HuangZhong",29,65,85,100)],

    dtype=persontype)

ages = peoples[:]['age']

chineses = peoples[:]['chinese']

maths = peoples[:]['math']

englishs = peoples[:]['english']
# 计算平均值使用  np.mean

print(np.mean(ages),"\n", np.mean(chineses)  ,"\n", np.mean(maths) ,"\n",np.mean(englishs)) 

x1 = np.arange(1,11,2)

x2 = np.linspace(1,9,5)
# 通过 NumPy 可以自由地创建等差数组，同时也可以进行加、减、乘、除、求 n 次方和取余数。
print(np.add(x1, x2),"\n", np.subtract(x1, x2)  ,"\n", np.multiply(x1, x2) ,"\n",np.divide(x1, x2)) 
print(np.power(x1, x2),"\n", np.remainder(x1, x2))

a = np.array([[4,3,2],[2,4,1]])
print(np.sort(a),"\n",np.sort(a, axis=None))
print(np.sort(a, axis=0),"\n",np.sort(a, axis=1))
