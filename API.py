#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/17 20:41 
# @Author : Patrick 
# @File : API.py
# @Software: PyCharm

import time

from requests import get
from requests import post

from Eval import checkstatus


class Game:
    def __init__(self):
        self.target = 6
        self.boardSize = 12
        self.time = 30
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
        # TODO: 纯对战记得改
        c, res = True, {'code': 'FAIL'}
        while res['code'] == 'FAIL':
            # if c:
            #     tmp = list(input('Please input TeamID1 and TeamID2 (ID1 ID2): ').split(' '))
            #     c = False
            # else:
            #     print('Error occurs. Please input again.')
            #     tmp = list(input('Please input TeamID1 and TeamID2 (ID1 ID2): ').split(' '))
            # tid1, tid2 = tmp[0], tmp[1]
            team_l = '1105 1089'

            tid1, tid2 = '1105', '1089'
            j = {'type': 'game', 'teamId1': tid1, 'teamId2': tid2, 'gameType': 'TTT',
                 'target': self.target, 'boardSize': self.boardSize}
            res = post('http://www.notexponential.com/aip2pgaming/api/index.php',
                       data=j,
                       headers=self.header)
            res = res.json()
            print('Create Game Successfully! GameID= ' + str(res['gameId']))
            if team_l.split()[0] == '1105':
                return True
            else:
                return False
        # return str(res['gameId'])

    def get_moves(self, gid):
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
        l = [list(i) for i in res_j['output'].split('\n')][:self.boardSize]
        print('   ' + '   '.join([str(k) for k in range(self.boardSize)]))
        for i in range(len(l)):
            print(str(i), end='')
            for j in range(len(l[i])):
                print('| ' + str(l[i][j]), end=' ')
            print('\n')
        # print(res_j['output'])
        return l

    def move(self, gid, m):
        # tmp = list(input('Please input TeamID and your move (TeamID Move): ').split(' '))
        # tid, m = tmp[0], tmp[1]
        # m = input('Please input your next move : ')
        # j = {'type': 'move', 'gameId': gid, 'teamId': '1105', 'move': m}
        j = {'type': 'move', 'gameId': gid, 'teamId': '1105', 'move': m}
        res = post('http://www.notexponential.com/aip2pgaming/api/index.php?',
                   data=j,
                   headers=self.header)
        res_j = res.json()
        if res_j['code'] == 'FAIL':
            print(res_j.get('message', 'Can\'t make such move.') + '\n')

    def start_game(self, first):
        if first:
            from Eval import findmin as find
        else:
            from Eval import findmax as find
        i = 0
        gid = input('Please input GameID: ')
        while True:
            res = get('http://www.notexponential.com/aip2pgaming/api/index.php?type=boardString&gameId=' + gid,
                      headers=self.header)
            if res.json().get('code') == 'OK':
                break
            else:
                gid = input('Invalid GameId. Please input GameID: ')
        list_map = self.show_board(gid)
        while True:
            a, b = find(list_map, self.target)
            print(a, b, i)
            m = str(a) + ',' + str(b)
            self.move(gid, m)
            list_map = self.show_board(gid)
            checkstatus(list_map, self.target)
            i += 1
            time.sleep(self.time)


g = Game()
while True:
    step = g.menu()
    if step == 1:
        first = g.create_game()
    elif step == 2:
        print(g.start_game(first))
    else:
        print('Function invalid. Please input again!\n')
