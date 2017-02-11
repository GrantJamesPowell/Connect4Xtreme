from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.
width = 7
depth = 6
empty_board = [[0] * width for _ in range(depth)]

# empty_board
# [[0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0]]
# indexed through BoardObject[row][column]
# human player is marked by 1, computer player is marked by 2


class GameBoard(models.Model):
    game_data = models.CharField(max_length=140, default=json.dumps(empty_board))

    def get_game_board(self):
        return json.loads(self.game_data)

    def __set_game_board(self, board):
        self.game_data = json.dumps(board)

    def make_move(self, player, slot):
        board = self.get_game_board()
        if board[0][slot]:  # This means that that slot was full, so this is an error
            return 1  # Error
        for i in reversed(range(depth)):
            if not board[i][slot]:
                board[i][slot] = player
                break
        self.__set_game_board(board)

    def has_winner(self):
        return False


class Game(models.Model):
    user = models.ForeignKey(User)
    isusersturn = models.BooleanField(default=0)  #  0 if computer's turn 1 is user's turn
    gameboard = models.OneToOneField(GameBoard)
