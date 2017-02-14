__author__ = 'grantpowell'

# Like AlphaGo But Better

from .models import GameBoard
import random

def ai_simple_move(game_board, player):
    # looks ahead one move!

    other_player = 1 if player == 2 else 2  # using the assumption there are 2 players

    # if there are no available moves then return None
    if not game_board.available_moves:
        return None

    # if there is a winning move take it
    player_moves = game_board.get_winning_moves(player)
    if player_moves:
        return random.choice(player_moves)

    # if the other player can win, block them
    other_player_winning_moves = game_board.get_winning_moves(other_player)
    if other_player_winning_moves:
        return random.choice(other_player_winning_moves)

    # get the moves that won't give the opponent a victory
    possible_moves = [move for move in game_board.available_moves
                     if not will_give_other_player_victory(game_board, player, move)]

    # pick from the moves that won't give victory, if there aren't any then just pick at random
    available_moves = possible_moves if possible_moves else game_board.available_moves

    # pick from the available moves with a preference for the middle
    width = len(available_moves)
    # normal distribution with a mu = width / 2 and a std = 1.5
    # it is modded by the width to make sure it falls within the game board
    move = round(random.normalvariate(width / 2, 1.5)) % width
    return available_moves[move]


def ai_advanced_move(game_board, player):

    other_player = 1 if player == 2 else 2  # using the assumption there are 2 players

    # if there are no available moves then return None
    if not game_board.available_moves:
        return None

    # if there is a winning move take it
    player_moves = game_board.get_winning_moves(player)
    if player_moves:
        return random.choice(player_moves)

    # if the other player can win, block them
    other_player_winning_moves = game_board.get_winning_moves(other_player)
    if other_player_winning_moves:
        return random.choice(other_player_winning_moves)

    # see what possible moves we can make from this position, looking to see if any of them will
    # immediately let the other player will
    possiblemoves = [move for move in game_board.available_moves
                     if not will_give_other_player_victory(game_board, player, move)]

    # if there aren't any possible moves where we can win, just admit defeat
    if len(possiblemoves) <= 1:
        return random.choice(game_board.available_moves)

    children = [GameBoard() for _ in possiblemoves]
    for num,move in enumerate(possiblemoves):
        children[num].make_move(player, move)




def will_give_other_player_victory(gameboard, player, move):
    # Test whether the resulting move will give other player victory
    other_player = 1 if player == 2 else 2
    testboard = GameBoard()
    testboard.game_data = gameboard.game_data
    testboard.make_move(player, move)
    if testboard.get_winning_moves(other_player):
        return True
    else:
        return False


def move_will_not_allow_other_player_to_force_defeat(gameboard, player, move):
    other_player = 1 if player == 2 else 2
    # pretend to make the proposed move
    inital_move_board = GameBoard(game_data=gameboard.game_data)
    inital_move_board.make_move(player, move)
    # make a possible board for each of the opponents possible moves, then check to see if the opponent move would
    # allow for them to have two places to win, while the current player has no way to win (i.e. its fine for the
    # opponent to have two ways to win if they give us a way to win on the next turn, else we don't want them to have
    # two ways to win)
    for move in inital_move_board.available_moves:
        opponent_move_board = GameBoard.objects.create(game_data=inital_move_board.game_data)
        opponent_move_board.make_move(other_player, move)
        player_has_winning_move = opponent_move_board.get_winning_moves(player)
        opponent_has_two_winning_moves = len(opponent_move_board.get_winning_moves(other_player)) >= 2
        if not player_has_winning_move and opponent_has_two_winning_moves:
            return False
    return True