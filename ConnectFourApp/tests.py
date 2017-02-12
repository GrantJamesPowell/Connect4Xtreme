from django.test import TestCase
from .models import GameBoard, Game

# Create your tests here.


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

    def test_veritical_victory(self):
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

    def test_winning_moves(self):
        pass



