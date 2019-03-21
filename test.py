#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/21 15:07 
# @Author : Patrick 
# @File : test.py 
# @Software: PyCharm

header = {
    'x-api-key': 'b9807dd3d0194262458e',
    'userid': '698'
}

tid1 = '1105'
tid2 = '1089'
target = '6'
boardSize = '20'

# j = {'type': 'game', 'teamId1': tid1, 'teamId2': tid2, 'gameType': 'TTT',
#      'target': target, 'boardSize': boardSize}
# res1 = requests.post('http://www.notexponential.com/aip2pgaming/api/index.php',
#                      data=j,
#                      headers=header)
# print(res1.json())
# res = requests.get(
#     'http://www.notexponential.com/aip2pgaming/api/index.php?type=boardString&gameId=' + str(res1.json()['gameId']),
#     headers=header)
# print(res.json()['output'])
# a = [[str(1), str(2)), (str(2), str(3))][True]


a = 10
b = 20
a = a ^ b
b = a ^ b
a = a ^ b
print(a)
print(b)
