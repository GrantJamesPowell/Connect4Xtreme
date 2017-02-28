__author__ = 'grantpowell'

import requests
import getpass
import re
import json

def availablemoves(board):
    return tuple(i for i in range(7) if board[0][i] == 0)

# get username and password
print()
username = input('Username:  ')
password = getpass.getpass()
print(chr(27) + "[2J")  # the clear terminal code

csrfpattern = re.compile("name='csrfmiddlewaretoken' value='(.*?)' />")

with requests.Session() as s:
    # login
    r = s.get('https://connect4xtreme.com/')
    csrftoken = csrfpattern.findall(r.text)
    csrftoken = csrftoken[0]
    r = s.post('https://connect4xtreme.com/login/', headers = {'referer': 'https://connect4xtreme.com/login/'},
               data= {'username': username, 'password': password, 'csrfmiddlewaretoken': csrftoken})
    # login successful!
    # set the inital game data
    r = s.get('https://connect4xtreme.com/gamedata')
    curdata = r.json()
    game = curdata['game']
    game_url = 'https://connect4xtreme.com/gamedata/{}'.format(game)
    csrf_token = curdata['csrf_token']
    while 1:  # main game loop
        # display the current game board
        board = json.loads(curdata['gameboard'])
        # super ugly color the game board comprehension
        str_board = '\n'.join([', '.join([str(i).replace('1', '\x1b[6;30;46m1\x1b[0m').replace('2', '\x1b[3;32;41m2\x1b[0m') for i in row]) for row in board])
        print()
        print(curdata['gamestr'])
        print()
        print(str_board)
        print('===================')
        print('0  1  2  3  4  5  6  ')
        print('===================')
        # if there is a winner display and break
        is_winner = int(curdata['winner'])
        if is_winner:
            print()
            print('winner is {}'.format(('No One', 'Human', 'Computer')[is_winner]))
            print()
            break
        # else get the next move
        move = -1
        while 1:
            move = input('Move (0-6):  ')
            if int(move) in availablemoves(board):
                break
            print('invalid move')
        # now that we have a valid move, we send that data in a post request to the server
        r = s.post(game_url, headers={'referer': game_url}, data={'move': move,
                                                                  'game': game,
                                                                  'difficulty': 0,
                                                                  'csrfmiddlewaretoken': csrf_token})
        curdata = r.json()
        print(chr(27) + "[2J")

print('Good Bye')


