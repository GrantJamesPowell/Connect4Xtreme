from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.
width = 7
depth = 6
needed_to_win = 4
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
    moves_data = models.CharField(max_length=40, default='')
    # if you increase the game board, you would need a larger max_length of game_data
    winner = models.IntegerField(default=0)

    #static Properties
    width = width
    depth = depth
    needed_to_win = needed_to_win

    def get_game_board(self):
        return json.loads(self.game_data)

    def __set_game_board(self, board):
        self.game_data = json.dumps(board)

    def make_move(self, player, slot):
        # error if the game is over
        if self.winner:
            return 1
        board = self.get_game_board()
        if board[0][slot]:  # This means that that slot was full, so this is an error
            return 1  # Error
        for i in reversed(range(depth)):
            if not board[i][slot]:  # this means that that slot has a 0 in it (i.e. is unused)
                board[i][slot] = player  # mark the lowest open row of the column with the player number
                break
        self.moves_data += str(slot)
        self.__set_game_board(board)  # set the game board property of the object
        self.winner = self.find_winner(board)  # set the winner if there is one

    @property
    def moves_list(self):
        return self.moves_data

    @property
    def moves_so_far(self):
        return sum(sum([bool(i) for i in row]) for row in self.get_game_board())

    @property
    def stalemate(self):
        board = self.get_game_board()
        no_winner = self.winner == 0
        no_moves_remaining = all(board[0])  # no 0s in the top row
        return no_winner and no_moves_remaining

    @property
    def available_moves(self):
        board = self.get_game_board()
        toprow = board[0]
        return [i for i in range(width) if toprow[i] == 0]  # return a list of the indexes that are empty

    @staticmethod
    def find_winner(board):

        # check columns for winner
        for col in range(width):  # iterate through the columns
            # iterate through the starting depths, if there is a max depth of 6 that means we only have to check
            # starting at depth 0, 1, 2 because at depth 3 there wouldn't be enough to have a connect 4
            for pos in range(depth + 1 - needed_to_win):  # you need plus one because range is weird
                # then we check if the first position is a zero, if it is that means that it can't be a connect four
                # beacuse there is an empty spot, this is to take care of the case where all 4 of positions
                # we are checking are the same but empty
                if board[pos][col] != 0:
                    # The hash set adds values to itself for every unique value, if at the end there was only one
                    # unique value, that means that all the elements were the same, which
                    # means that there was a winner
                    group = [board[i][col] for i in range(pos, pos + needed_to_win)]
                    uniquevals = set(group)
                    if len(uniquevals) == 1:
                        # return the unique element which is equal to the player number
                        return board[pos][col]

        # check the rows for a winner
        for row in board:
            # iterate through the row for every start position with enough length remaining to have a winner.
            # For a 7 width game we would only need to look at positions 0,1,2,3 because position 4 would only
            # have 3 slots left in the row, so it couldn't have a connect 4
            for pos in range(width + 1 - needed_to_win):
                # check to make sure that the first spot isn't empty, if they were all the same but empty, we wouldn't
                # have a want to return 0 as the winner
                if row[pos] != 0:
                    # check to see that the number of unique entries is equal to one
                    if len(set(row[pos: pos + needed_to_win])) == 1:
                        # return the first entry, equal to the player number
                        return row[pos]

        # check right diagonals for a winner (diagonal where the lowest piece is the farthest right)
        for row in range(depth + 1 - needed_to_win):
            for col in range(width + 1 - needed_to_win):
                if board[row][col] != 0:  # check to make sure the first value isn't empty
                    group = [board[row + offset][col + offset] for offset in range(needed_to_win)]  # iterate diagonally
                    uniquevals = set(group)
                    if len(uniquevals) == 1:  # there was only one unique value in the group
                        return board[row][col]  # return the unique value


        # check left diagonals for a winner (diagonal where the lowest piece is the farthest left)
        for row in range(depth + 1 - needed_to_win):
            for col in range(width - 1, needed_to_win - 2, -1):
                if board[row][col] != 0:
                    group = [board[row + offset][col - offset] for offset in range(needed_to_win)]
                    uniquevals = set(group)
                    if len(uniquevals) == 1:
                        return board[row][col]

        # no winner was found
        return 0

    def get_winning_moves(self, player):
        winning_moves = []
        # try all the moves in a width
        for move in range(width):
            # make a "testboard" based on the current board
            testboard = GameBoard()
            testboard.game_data = self.game_data
            testboard.make_move(player, move)
            if testboard.winner == player:
                winning_moves.append(move)
        return winning_moves

    def number_of_players_moves(self, player):
        board = self.get_game_board()
        return sum(sum([bool(i) for i in row if i == player]) for row in board)

    @property
    def GameObj(self):
        return Game.objects.filter(gameboard=self).first()


class Game(models.Model):
    user = models.ForeignKey(User)
    isusersturn = models.BooleanField(default=0)  # 0 if computer's turn 1 is user's turn
    gameboard = models.OneToOneField(GameBoard)
    starttime = models.DateField(auto_now=True)
    hardmode = models.BooleanField(default=0)  # 0 for easy, 1 for hard

    @property
    def status(self):
        if self.gameboard.winner:
            return ['Lost', 'Won'][self.gameboard.winner == 1]
        if self.gameboard.stalemate:
            return 'Stalemate'
        else:
            return 'Your Move'

    @property
    def level(self):
        return ['Normal', 'X-treme'][self.hardmode]

    def __str__(self):
        return '{} Game {} ({})'.format(self.level, self.starttime, self.status)

