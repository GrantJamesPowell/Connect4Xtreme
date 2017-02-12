from django.test import TestCase
from .models import GameBoard, Game
from .alphaconnectfour import ai_simple_move

import random

# Create your tests here.


class AlphaConnectFourSimpleAiTests(TestCase):

    def test_simple_take_win_if_available(self):
        board = GameBoard()
        player = 1
        for _ in range(3):
            board.make_move(player, 0)
        move = ai_simple_move(board, player)
        self.assertTrue(move == 0)

    def test_simple_block_if_other_player_can_win(self):
        board = GameBoard()
        player = 1
        other_player = 2
        for _ in range(3):
            board.make_move(player,0)
        move = ai_simple_move(board, other_player)
        self.assertTrue(move == 0)

    def test_generate_100_moves_and_make_sure_they_are_valid_for_no_winner_yet_not_full_board(self):
        for _ in range(100):
            board = GameBoard()
            for _ in range(3):
                board.make_move(1, random.randint(0, board.width - 1))
                board.make_move(2, random.randint(0, board.width - 1))
            move = ai_simple_move(board, 1)
            self.assertTrue(move in board.available_moves)

            error = board.make_move(1, move)
            self.assertEqual(error, None)

    def test_simple_ai_play_against_itself_100_times(self):
        for _ in range(100):
            board = GameBoard()
            turn = 0
            players = (1,2)
            while not board.winner and not board.stalemate:
                move = ai_simple_move(board, players[turn])
                if move is not None:
                    board.make_move(players[turn], move)
                    turn = not turn


        print()
        print('Simple Ai Game Example')
        for row in board.get_game_board(): print(row)
        print()


class GameBoardTests(TestCase):

    def test_invalid_move(self):
        board = GameBoard()
        moves = (0,0,0,0,0,0)  # Fill a Column
        player = 1
        for move in moves:
            error = board.make_move(player, move)
            self.assertEqual(error, None)  # assert there is no error
        move = 0  # add one to a filled row
        error = board.make_move(player, move)
        self.assertEqual(error, 1)

    def test_stalemate(self):
        board = GameBoard()
        evens = (0,2,4,6)
        odds = (1,3,5)
        for _ in range(3):
            for move in evens:
                board.make_move(1, move)
            for move in odds:
                board.make_move(2, move)
        for _ in range(3):
            for move in odds:
                board.make_move(1, move)
            for move in evens:
                board.make_move(2, move)
        self.assertTrue(board.stalemate)

    def test_horizontal_victory(self):
        board = GameBoard()
        player = 1
        moves = (0,1,2,3)
        for move in moves:
            board.make_move(player, move)
        self.assertEqual(player, board.winner)

    def test_vertical_victory(self):
        board = GameBoard()
        player = 1
        moves = (0,0,0,0)
        for move in moves:
            board.make_move(player, move)
        self.assertEqual(player, board.winner)

    def test_right_diagonal_win(self):
        board = GameBoard()
        p2moves = (0,0,0,1,1,2)  # make a little triangle to put the winning diagonal on
        p1moves = (0,1,2,3)
        for move in p2moves:
            board.make_move(2, move)
        for move in p1moves:
            board.make_move(1, move)
        self.assertEqual(board.winner, 1)

    def test_left_diagonal_win(self):
        board = GameBoard()
        p2moves = (3,3,3,2,2,1)
        p1moves = (3,2,1,0)
        for move in p2moves:
            board.make_move(2, move)
        for move in p1moves:
            board.make_move(1, move)
        self.assertEqual(board.winner, 1)

    def test_winning_moves_horizontal(self):
        board = GameBoard()
        moves = (0,1,2)
        for move in moves:
            board.make_move(1, move)
        winning_moves = board.get_winning_moves(1)
        self.assertTrue(3 in winning_moves)

    def test_winning_moves_vertical(self):
        board = GameBoard()
        moves = (0,0,0)
        for move in moves:
            board.make_move(1, move)
        winning_moves = board.get_winning_moves(1)
        self.assertTrue(0 in winning_moves)

    def test_winning_moves_diagonal(self):
        board =GameBoard()
        p2moves = (0,0,0,1,1,2)  # make a little triangle to put the winning diagonal on
        p1moves = (0,1,2)
        for move in p2moves:
            board.make_move(2, move)
        for move in p1moves:
            board.make_move(1, move)
        winning_moves = board.get_winning_moves(2)
        self.assertTrue(3 in winning_moves)


