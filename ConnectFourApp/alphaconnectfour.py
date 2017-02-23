__author__ = 'grantpowell'

# Like AlphaGo But Better

from .models import GameBoard
import random

def ai_simple_move(game_board, player):
    # looks ahead one move!

    other_player = 1 if player == 2 else 2

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

    other_player = 1 if player == 2 else 2

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
    # immediately let the other player win
    look_ahead_2_moves = [move for move in game_board.available_moves
                          if not will_give_other_player_victory(game_board, player, move)]

    # look ahead and see if any of the possible moves will allow the opponent to force a win
    look_ahead_3_moves = [move for move in look_ahead_2_moves if
                          move_will_not_allow_other_player_to_force_defeat(game_board, player, move)]

    # Analyze the moves returned from look 3 moves ahead and pick the one that has the highest amount of "groups"
    # That can possibly lead to a connect 4, also subtracting points if the other player has opportunities
    if look_ahead_3_moves:
        best_move = max(look_ahead_3_moves, key=lambda move: board_score(game_board, player, move))
        if best_move:
            return best_move

    # we couldn't get a best move so pick from the first set of moves that had any valid moves in them
    # pick from the moves that won't give victory, if there aren't any then just pick at random
    available_moves = look_ahead_3_moves or look_ahead_2_moves or game_board.available_moves

    # pick from the available moves with a preference for the middle
    width = len(available_moves)
    # normal distribution with a mu = width / 2 and a std = 1.5
    # it is modded by the width to make sure it falls within the game board
    move = round(random.normalvariate(width / 2, 1.5)) % width
    return available_moves[move]





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
        opponent_move_board = GameBoard(game_data=inital_move_board.game_data)
        opponent_move_board.make_move(other_player, move)
        player_has_winning_move = opponent_move_board.get_winning_moves(player)
        opponent_has_two_winning_moves = len(opponent_move_board.get_winning_moves(other_player)) >= 2
        if not player_has_winning_move and opponent_has_two_winning_moves:
            return False
    return True



def board_score(game_board, player, move):
    other_player = 1 if player == 2 else 2
    test_board = GameBoard(game_data=game_board.game_data)
    test_board.make_move(player, move)

    score = 0
    for group in test_board.iter_all_groups():
        group_without_zeros = [pos for pos in group if pos != 0]
        # if the entire group is zeros, then we don't need to check it
        if not group_without_zeros:
            continue
        # if there are more than one player in this group it can't be a connect 4 so don't add it to the score
        if len(set(group_without_zeros)) >= 2:
            continue
        # if the moves are all for the player, add them to the score as a positive
        if group_without_zeros[0] == player:
            score += len(group_without_zeros)
        # if the moves are for the other player then subtract them from the board score
        elif group_without_zeros[0] == other_player:
            score -= len(group_without_zeros)

    # prefer moves closer to the middle by giving them a slightly higher score
    adjustment = abs((test_board.width - 1) - move) * .01

    return score + adjustment
