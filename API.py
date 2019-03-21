#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/17 20:41 
# @Author : Patrick 
# @File : API.py
# @Software: PyCharm

from requests import get
from requests import post

from Evaluation_Function import evaluation_Function as minimax


# from import as


class Game:
    def __init__(self):
        self.target = 6
        self.boardSize = 12
        self.header = {
            'x-api-key': 'b9807dd3d0194262458e',
            'userid': '698'
        }

    @staticmethod
    def menu():
        print('---------------------------------\n'
              'Menu:\n'
              '1. Create a Game\n'
              '2. Start Game\n'
              '---------------------------------'
              )
        return int(input('Please select function: '))

    def create_game(self):
        c, res = True, {'code': 'FAIL'}
        while res['code'] == 'FAIL':
            if c:
                tmp = list(input('Please input TeamID1 and TeamID2 (ID1 ID2): ').split(' '))
                c = False
            else:
                print('Error occurs. Please input again.')
                tmp = list(input('Please input TeamID1 and TeamID2 (ID1 ID2): ').split(' '))
            tid1, tid2 = tmp[0], tmp[1]
            j = {'type': 'game', 'teamId1': tid1, 'teamId2': tid2, 'gameType': 'TTT',
                 'target': self.target, 'boardSize': self.boardSize}
            res = post('http://www.notexponential.com/aip2pgaming/api/index.php',
                       data=j,
                       headers=self.header)
            res = res.json()
        print('Create Game Successfully! GameID= ' + str(res['gameId']))

    def get_moves(self, gid, count):
        count = '20'
        res = get(
            'http://www.notexponential.com/aip2pgaming/api/index.php?type=moves&gameId=' + gid + '&count=+' + count,
            headers=self.header)
        # print(res.json())
        return res.json()['moves']  # list[dict]

    def get_map(self, gid):
        res = get('http://www.notexponential.com/aip2pgaming/api/index.php?type=boardMap&gameId=' + gid,
                  headers=self.header)
        return res.json()['output']

    def show_board(self, gid):
        res = get('http://www.notexponential.com/aip2pgaming/api/index.php?type=boardString&gameId=' + gid,
                  headers=self.header)
        res_j = res.json()
        l = [list(i) for i in res_j['output'].split('\n')]
        # print(res_j['output'])
        return l[:13]

    def move(self, gid, tid, m):
        # tmp = list(input('Please input TeamID and your move (TeamID Move): ').split(' '))
        # tid, m = tmp[0], tmp[1]
        # m = input('Please input your next move : ')
        # j = {'type': 'move', 'gameId': gid, 'teamId': '1105', 'move': m}
        j = {'type': 'move', 'gameId': gid, 'teamId': tid, 'move': m}
        res = post('http://www.notexponential.com/aip2pgaming/api/index.php?',
                   data=j,
                   headers=self.header)
        res_j = res.json()
        if res_j['code'] == 'FAIL':
            # print(res_j)
            # print(res_j.get('message', 'null'))
            print(res_j.get('message', 'Can\'t make such move.') + '\n')

    def start_game(self):
        gid = input('Please input GameID: ')
        while True:
            res = get('http://www.notexponential.com/aip2pgaming/api/index.php?type=boardString&gameId=' + gid,
                      headers=self.header)
            if res.json().get('code') == 'OK':
                break
            else:
                gid = input('Invalid GameId. Please input GameID: ')
        while True:
            i = 0
            list_map = self.show_board(gid)
            m = [minimax(list_map, self.target), (self.boardSize // 2, self.boardSize // 2)][i == 0]
            if m == 'X':
                return 'X wins'
            elif m == 'O':
                return 'O wins'
            tid = ['1089', '1105'][i % 2 == 0]
            self.move(gid, tid, m)
            i += 1


g = Game()
while True:
    step = g.menu()
    if step == 1:
        g.create_game()
    elif step == 2:
        print(g.start_game())
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
