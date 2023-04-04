import copy
import math
from typing import Tuple, List

from two_player_games.player import Player
from two_player_games.games.connect_four import ConnectFour, ConnectFourMove

import time

import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7


class MinMaxSolver:

    def __init__(self, depth, game: ConnectFour):
        self.game = game
        self.depth = depth
        self.pointMatrix = []

        x = len(game.state.fields)
        y = len(game.state.fields[0])
        self.generate_point_matrix(y, x)

    def generate_point_matrix(self, height, width):
        """
        Generates martix holding amount of possible 4's
        that a given cell can take part in. For example
        Corners have value 3 (on at least 4x4 board)

        Example for 6x7:
        [[3  4  5  7  5  4  3]
        [4  6  8 10  8  6  4]
        [5  8 11 13 11  8  5]  - it is worth placing in center
        [5  8 11 13 11  8  5]
        [4  6  8 10  8  6  4]
        [3  4  5  7  5  4  3]]
        """

        self.pointMatrix = [[0 for y in range(height)] for x in range(width)]

        for ci, column in enumerate(self.pointMatrix):

            possibleHorizontals = max(
                0, min(ci+3, width-1)-max(0, ci-3)-3)+1

            for ri, row in enumerate(column):
                # right span-left span-3

                possibleVerticals = max(
                    0, min(ri+3, height-1)-max(0, ri-3)-3)+1

                x, y = ri, ci
                sx, sy = x-3, y-3
                while sx < 0 or sy < 0:
                    sx += 1
                    sy += 1

                ex, ey = x+3, y+3

                while ex >= height or ey >= width:
                    ex -= 1
                    ey -= 1

                possibleSkewers1 = max(0, ex-sx-3+1)

                sx, sy = x-3, y+3
                while sx < 0 or sy >= width:
                    sx += 1
                    sy -= 1

                ex, ey = x+3, y-3

                while ex >= height or ey < 0:
                    ex -= 1
                    ey += 1

                possibleSkewers2 = max(0, ex-sx-3+1)
                self.pointMatrix[ci][ri] = possibleHorizontals + \
                    possibleVerticals+possibleSkewers1+possibleSkewers2

    def evaluate_position(self, depth, isfinish) -> float:

        winner = isfinish
        if winner is True:
            return 0  # draw
        elif winner:  # not false

            if winner.char == self.game.first_player.char:
                # player 1 won -> board evaluation is known to be inf
                # add depth, the more depth left, the faster poskładał tego drugiego
                return 10000+depth
            else:
                # player 2 won
                # subtract depth, penalty for not defending
                return -10000-depth

        # game in progress, return heuristic value
        return self.rate_board()

    def rate_board(self):
        """
        For each spot on board adds/subtracts points based on pointMask,
        depending whose piece is there
        """
        total = 0
        for ci, column in enumerate(self.game.state.fields):
            for ri, piece in enumerate(column):
                if piece is not None:
                    total += self.pointMatrix[ci][ri] * \
                        (1 if piece.char == self.game.first_player.char else -1)
        return total

    def minimax(self, depth, alpha: float, beta: float, is_maximizing_player: bool, lastmove=None) -> Tuple[int, float]:
        """Returns column index and score"""

        # either returns winning player, or bool True=draw, False=not finished
        isfinish = self.optimal_is_finished(lastmove)

        if depth == 0 or isfinish:
            res = self.evaluate_position(depth, isfinish)
            return None, res

        # recursive step
        else:
            # this is safe because game is not finished
            bestmove = self._get_valid_locations()[0]

            funct = max if is_maximizing_player else min

            # start with worst value
            best = -math.inf if is_maximizing_player else math.inf

            for move in self._get_valid_locations():
                self.game.make_move(ConnectFourMove(move))
                result = self.minimax(
                    depth-1, alpha, beta, not is_maximizing_player, move)[1]
                self.revert_move(move)

                if not is_maximizing_player:
                    # the idea is that opponent tells me what he knows
                    # is the best move (through alpha beta params)
                    # so I dont have to keep looking for better moves
                    # as he will not play this anyway
                    if result <= alpha:
                        return move, result
                    beta = min(beta, result)
                else:
                    if result >= beta:
                        return move, result
                    alpha = max(alpha, result)

                # if it's the best, update variables
                if result == funct(result, best) and result != best:
                    best = result
                    bestmove = move
            return bestmove, best

    def revert_move(self, move):
        # remove element at the top of this row

        try:
            height = self.game.state.fields[move].index(None)-1
        except:
            height = ROW_COUNT-1
        # remove piece
        self.game.state.fields[move][height] = None
        # swap player turns
        self.game.state._current_player, self.game.state._other_player = self.game.state._other_player, self.game.state._current_player

    def get_best_move(self, lastmove=None) -> int:
        isFirstPlayer = self.game.get_current_player().char == self.game.first_player.char
        move, value = self.minimax(
            self.depth, -math.inf, math.inf, isFirstPlayer, lastmove)
        print("best move", move, "evaluated at", value)
        return move

    def _get_valid_locations(self) -> List[int]:
        return self.game.get_moves()

    def _is_valid_move(self, col_index: int) -> bool:
        return col_index in self._get_valid_locations()

    def optimal_is_finished(self, lastmove):
        """
         Very fast check to figure out game state,
         check only the previous column top element possibilites
         Can return 2 types of values:
         * player (who won)
         * True - draw
         * False - game is still going
         """
        board = self.game.state.fields
        if lastmove is None:
            return all(map(all, board))
        c1 = self.game.first_player
        c2 = self.game.second_player

        # python throws index exception here
        try:
            height = board[lastmove].index(None)-1
        except:
            height = ROW_COUNT-1

        # [ymin,ymax,xmin,xmax] - area of possible places
        rect = [max(0, height-3), min(height+3, ROW_COUNT-1), max(0, lastmove-3),
                min(lastmove+3, COLUMN_COUNT-1)]

        # check row
        run = 0
        for i in range(rect[2], rect[3]+1):
            if board[i][height] == c1:
                run = max(1, run+1)
            elif board[i][height] == c2:
                run = min(-1, run-1)
            else:
                run = 0
            if run in (4, -4):
                return c1 if run == 4 else c2

        # check column, only top 4
        top4 = board[lastmove][rect[0]: height+1]
        if top4 == [c1]*4:
            return c1
        elif top4 == [c2]*4:
            return c2

        # diagonals
        # from bottom left
        x, y = lastmove, height
        dist = 0
        while x != 0 and y != 0 and dist != 3:
            x -= 1
            y -= 1
            dist += 1

        run = 0
        for i in range(4+dist):
            if x+i >= COLUMN_COUNT or y+i >= ROW_COUNT:
                break
            if board[x+i][y+i] == c1:
                run = max(1, run+1)
            elif board[x+i][y+i] == c2:
                run = min(-1, run-1)
            else:
                run = 0

            if run in (4, -4):
                return c1 if run == 4 else c2

        # from bottom right
        x, y = lastmove, height
        dist = 0
        run = 0
        while x < COLUMN_COUNT-1 and y != 0 and dist != 3:
            x += 1
            y -= 1
            dist += 1

        for i in range(4+dist):
            if x-i <= -1 or y+i >= ROW_COUNT:
                break
            if board[x-i][y+i] == c1:
                run = max(1, run+1)
            elif board[x-i][y+i] == c2:
                run = min(-1, run-1)
            else:
                run = 0

            if run in (4, -4):
                return c1 if run == 4 else c2

        return all(map(all, board))


def interactive():
    p1 = Player("a")  # maximising
    p2 = Player("b")  # minimising
    game = ConnectFour(size=(COLUMN_COUNT, ROW_COUNT),
                       first_player=p1, second_player=p2)

    difficulty = int(input("Type difficulty:"))
    solver = MinMaxSolver(difficulty, game)

    while not solver.game.is_finished():

        # calculate best
        print(solver.game)
        best = solver.get_best_move()
        solver.game.make_move(ConnectFourMove(best))

        if (solver.game.is_finished()):
            break

        print(solver.game)
        move = int(input("Your move:"))
        solver.game.make_move(ConnectFourMove(move))
    print(solver.game)
    if solver.game.get_winner():
        print("Player", solver.game.get_winner().char, "won")
    else:
        print("Draw")


# Simulation between two players, "a" always starts
def TwoDifferentComputers():
    p1 = Player("a")  # maximising
    p2 = Player("b")  # minimising
    game = ConnectFour(size=(COLUMN_COUNT, ROW_COUNT),
                       first_player=p1, second_player=p2)

    depths = [5, 5]  # first, second player
    solver = MinMaxSolver(depths[0], game)  # first player starts
    start = time.time()
    best = 0
    current_player = 0
    while True:
        solver.depth = depths[current_player]
        best = solver.get_best_move(best)
        if best is None:
            break
        print("move", best)
        solver.game.make_move(ConnectFourMove(best))
        print(game)
        current_player = 1-current_player

    if solver.game.get_winner():
        print("Player", solver.game.get_winner().char, "won")
    else:
        print("Draw")

    print(time.time()-start, "seconds")


# TwoDifferentComputers()
# interactive()
