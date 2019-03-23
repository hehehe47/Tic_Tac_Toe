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
        self.target = 5
        self.boardSize = 12
        self.sleep = 1
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
            if tid1.split()[0] == '1105':
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
        # print(res_j['output'])
        return l

    def print_board(self, l):
        print('   ' + '   '.join([str(k) for k in range(self.boardSize)]))
        for i in range(len(l)):
            print(str(i), end='')
            for j in range(len(l[i])):
                print('| ' + str(l[i][j]), end=' ')
            print('\n')

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
        return self.show_board(gid)

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
        self.print_board(list_map)
        if not first:
            tmp_l = self.show_board(gid)
            while tmp_l == list_map:
                tmp_l = self.show_board(gid)
                time.sleep(self.sleep)

            list_map = tmp_l
            self.print_board(list_map)
        while True:
            a, b = find(list_map, self.target)
            m = str(a) + ',' + str(b)
            print('Move to ' + str(a) + ',' + str(b))
            list_map = self.move(gid, m)
            self.print_board(list_map)

            tmp_l = self.show_board(gid)
            while tmp_l == list_map:
                tmp_l = self.show_board(gid)
                time.sleep(self.sleep)

            list_map = tmp_l
            self.print_board(list_map)
            checkstatus(list_map, self.target)
            i += 1


g = Game()
f = False
while True:
    step = g.menu()
    if step == 1:
        first = g.create_game()
        f = True
    elif step == 2:
        if not f:
            first = input('Please input whether 1105 is first or second.\n'
                          'First input: True; Second input: False;\n'
                          'Whether True or False: ')
            while first != 'True' and first != 'False':
                print('Input error.')
                first = input('Please input whether 1105 is first or second.\n'
                              'First input: True; Second input: False;\n'
                              'Whether True or False: ')
        first = bool(first)
        print(g.start_game(first))
    else:
        print('Function invalid. Please input again!\n')
