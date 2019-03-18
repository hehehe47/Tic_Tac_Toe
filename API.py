#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/17 20:41 
# @Author : Patrick 
# @File : API.py
# @Software: PyCharm
import requests

from requests import post
from requests import get

header = {
    'x-api-key': 'b9807dd3d0194262458e',
    'userid': '698'
}
gid = None


def menu():
    print('---------------------------------\n'
          'Menu:\n'
          '1. Create a Game\n'
          '2. Start Game\n'
          '---------------------------------'
          )
    return int(input('Please select function: '))


def create_game():
    # TODO : Optimization
    #   other parameter

    c, res = True, {'code': 'FAIL'}
    while res['code'] == 'FAIL':
        if c:
            tmp = list(input('Please input TeamID1 and TeamID2 (ID1 ID2): ').split(' '))
            c = False
        else:
            print('Error occurs. Please input again.')
            tmp = list(input('Please input TeamID1 and TeamID2 (ID1 ID2): ').split(' '))
        tid1, tid2 = tmp[0], tmp[1]
        j = {'type': 'game', 'teamId1': tid1, 'teamId2': tid2, 'gameType': 'TTT'}
        res = post('http://www.notexponential.com/aip2pgaming/api/index.php',
                   data=j,
                   headers=header)
        res = res.json()
    print('Create Game Successfully! GameID= ' + str(res['gameId']))


def get_moves(gid, count):
    count = '20'
    res = get('http://www.notexponential.com/aip2pgaming/api/index.php?type=moves&gameId=' + gid + '&count=+' + count,
              headers=header)
    print(res.json())
    return res.json()['moves']  # list[dict]


def get_map(gid):
    res = get('http://www.notexponential.com/aip2pgaming/api/index.php?type=boardMap&gameId=' + gid,
              headers=header)
    return res.json()['output']


def show_board(gid):
    res = get('http://www.notexponential.com/aip2pgaming/api/index.php?type=boardString&gameId=' + gid,
              headers=header)
    res_j = res.json()
    print(res_j['output'])


def move(gid):
    tmp = list(input('Please input TeamID and your move (TeamID Move): ').split(' '))
    tid, m = tmp[0], tmp[1]
    # m = input('Please input your next move : ')
    # j = {'type': 'move', 'gameId': gid, 'teamId': '1105', 'move': m}
    j = {'type': 'move', 'gameId': gid, 'teamId': tid, 'move': m}
    res = post('http://www.notexponential.com/aip2pgaming/api/index.php?',
               data=j,
               headers=header)
    res_j = res.json()
    if res_j['code'] != 'FAIL':
        print(res_j)
        print(res_j.get('message', 'null'))
        show_board(gid)
        get_map(gid)
        get_moves(gid, 20)
    else:
        print(res_j.get('message', 'Can\'t make such move.') + '\n')


def start_game():
    # TODO: Remember to end game

    gid = input('Please input GameID: ')
    while True:
        res = get('http://www.notexponential.com/aip2pgaming/api/index.php?type=boardString&gameId=' + gid,
                  headers=header)
        if res.json().get('code') == 'OK':
            break
        else:
            gid = input('Invalid GameId. Please input GameID: ')
    while True:
        move(gid)


while True:
    step = menu()
    if step == 1:
        create_game()
    elif step == 2:
        start_game()
    else:
        print('Function invalid. Please input again!\n')

# # j = {'teamId': '1105', 'userId': '698', 'type': 'member'}
# # j = {'type': 'team','teamId': '1105'}
# j = {'type': 'game', 'teamId1': '1', 'teamId2': '1', 'gameType': 'TTT'}
# # j = {'type': 'move', 'teamId': '1041', 'gameId': '1082', 'move': '4,4'}
#
# r = requests.post(
#     'http://www.notexponential.com/aip2pgaming/api/index.php',
#     headers=header,
#     data=j)
# # r = requests.get('http://www.notexponential.com/aip2pgaming/api/index.php', json=j, headers=header)
# print(r)
# print(r.text)
# print(r.headers)
# # requests.get('http://http://www.notexponential.com/aip2pgaming/api/index.php',
# #              )
