from checkersDefined import CheckersBoard, play_against_mcts, play_against_random, random_player
from mcts import MCTS_Checkers


board = CheckersBoard()
mcts = MCTS_Checkers(board)
play_against_mcts(board, mcts, 100)