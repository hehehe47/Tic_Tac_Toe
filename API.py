#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/17 20:41 
# @Author : Patrick 
# @File : API.py
# @Software: PyCharm

# import libs
import time

from requests import get
from requests import post


class Game:
    def __init__(self):
        # initial parameter
        self.target = 6
        self.boardSize = 12
        self.sleep = 1
        # Personal API key
        self.header = {
            'x-api-key': 'b9807dd3d0194262458e',
            'userid': '698'
        }

    # create menu
    @staticmethod
    def menu():
        print('---------------------------------\n'
              'Menu:\n'
              '1. Create a Game\n'
              '2. Start Game\n'
              '---------------------------------'
              )
        return int(input('Please select function: '))

    # create game
    def create_game(self):
        # default parameter
        c, res = True, {'code': 'FAIL'}
        # if fail to create game, just loop until success
        while res['code'] == 'FAIL':
            if c:
                tmp = list(input('Please input TeamID1 and TeamID2 (ID1 ID2): ').split(' '))
                c = False
            else:
                print('Error occurs. Please input again.')
                tmp = list(input('Please input TeamID1 and TeamID2 (ID1 ID2): ').split(' '))
            tid1, tid2 = tmp[0], tmp[1]

            # send create game request
            j = {'type': 'game', 'teamId1': tid1, 'teamId2': tid2, 'gameType': 'TTT',
                 'target': self.target, 'boardSize': self.boardSize}
            res = post('http://www.notexponential.com/aip2pgaming/api/index.php',
                       data=j,
                       headers=self.header)
            res = res.json()
            # print Gameid
            print('Create Game Successfully! GameID= ' + str(res['gameId']))
            # judge whether 1105 is 1p or 2p
            if tid1.split()[0] == '1105':
                return True
            else:
                return False
        # return str(res['gameId'])

    # api for get moves
    def get_moves(self, gid):
        count = '20'
        res = get(
            'http://www.notexponential.com/aip2pgaming/api/index.php?type=moves&gameId=' + gid + '&count=+' + count,
            headers=self.header)
        # print(res.json())
        return res.json()['moves']  # list[dict]

    # api for get_map
    def get_map(self, gid):
        res = get('http://www.notexponential.com/aip2pgaming/api/index.php?type=boardMap&gameId=' + gid,
                  headers=self.header)
        return res.json()['output']

    # api for get_map_string
    def show_board(self, gid):
        res = get('http://www.notexponential.com/aip2pgaming/api/index.php?type=boardString&gameId=' + gid,
                  headers=self.header)
        res_j = res.json()
        # transform map_string to map[[]]
        return [list(i) for i in res_j['output'].split('\n')][:self.boardSize]
        # print(res_j['output'])

    # print current board line by line
    def print_board(self, l):
        print('   ' + '   '.join([str(k) for k in range(self.boardSize)]))
        for i in range(len(l)):
            print(str(i), end='')
            for j in range(len(l[i])):
                print('| ' + str(l[i][j]), end=' ')
            print('\n')

    # api for movez
    def move(self, gid, m):
        j = {'type': 'move', 'gameId': gid, 'teamId': '1105', 'move': m}
        res = post('http://www.notexponential.com/aip2pgaming/api/index.php?',
                   data=j,
                   headers=self.header)
        res_j = res.json()
        if res_j['code'] == 'FAIL':
            print(res_j.get('message', 'Can\'t make such move.') + '\n')
        return self.show_board(gid)

    # class method to start game
    # parameter: first: whether 1105 is 1p or not
    def start_game(self, first):
        if first:
            # if first, find the best move for player ‘O’
            from Eval import findmin as find
        else:
            # else, find the best move for player ‘X’
            from Eval import findmax as find
        i = 0

        # start game
        gid = input('Please input GameID: ')
        while True:
            res = get('http://www.notexponential.com/aip2pgaming/api/index.php?type=boardString&gameId=' + gid,
                      headers=self.header)
            if res.json().get('code') == 'OK':
                break
            else:
                # if game id is invalid
                gid = input('Invalid GameId. Please input GameID: ')

        # show the original board
        list_map = self.show_board(gid)
        self.print_board(list_map)

        # here is to fetch board after 1s
        # in order to find the opponent has made his move
        if not first:
            tmp_l = self.show_board(gid)
            # if two board equals, the opponent hasn't made move, go loop
            while tmp_l == list_map:
                tmp_l = self.show_board(gid)
                # sleep 1s
                time.sleep(self.sleep)

            list_map = tmp_l
            self.print_board(list_map)

        # start game infinite loop
        while True:
            # go to minimax find next move
            a, b = find(list_map, self.target)
            m = str(a) + ',' + str(b)
            print('Move to ' + str(a) + ',' + str(b))
            # post move
            list_map = self.move(gid, m)
            self.print_board(list_map)
            # here is to fetch board after 1s
            # in order to find the opponent has made his move
            tmp_l = self.show_board(gid)
            # if two board equals, the opponent hasn't made move, go loop
            while tmp_l == list_map:
                tmp_l = self.show_board(gid)
                # sleep 1s
                time.sleep(self.sleep)
            list_map = tmp_l
            self.print_board(list_map)
            # check if either player has won
            # if won, whole program exit
            # checkstatus(list_map, self.target)
            i += 1


# new Game class
g = Game()
# if start from step one
step_one = False
# infinite loop
while True:
    # create menu
    step = g.menu()
    if step == 1:
        # create game
        first = g.create_game()
        step_one = True
    elif step == 2:
        if not step_one:
            # need to indicate 1105 is 1p or 2p
            first = input('Please input whether 1105 is first or second.\n'
                          'First input: True; Second input: False;\n'
                          'Whether True or False: ')
            while first != 'True' and first != 'False':
                print('Input error.')
                first = input('Please input whether 1105 is first or second.\n'
                              'First input: True; Second input: False;\n'
                              'Whether True or False: ')
        first = bool(first)
        # start game
        print(g.start_game(first))
    else:
        print('Function invalid. Please input again!\n')
