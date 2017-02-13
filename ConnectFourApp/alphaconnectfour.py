__author__ = 'grantpowell'

# Like AlphaGo But Better

import random

def ai_simple_move(game_board, player):
    other_player = 1 if player == 2 else 2  # using the assumption there are 2 players

    # if there are no available moves then return None
    if not game_board.available_moves:
        return None

    # if there is a winning move take it
    ai_winning_moves = game_board.get_winning_moves(player)
    if ai_winning_moves:
        return random.choice(ai_winning_moves)

    # if the other player can win, block them
    other_player_winning_moves = game_board.get_winning_moves(other_player)
    if other_player_winning_moves:
        return random.choice(other_player_winning_moves)

    # else just select randomly, with a preference for the middle
    available_moves = game_board.available_moves
    width = len(available_moves)
    # normal distribution with a mu = width / 2 and a std = 1.5
    # it is modded by the width to make sure it falls within the game board
    move = round(random.normalvariate(width / 2, 1.5)) % width
    return available_moves[move]


def ai_advanced_move(game_board, player):
    # TODO: Implement this
    return ai_simple_move(game_board, player)
