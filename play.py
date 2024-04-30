from checkersDefined import CheckersBoard
from mcts import MCTS_Checkers
import random
import time

def random_player(other_team, current_board, last_move=None):
    players = ["blue", "red"]
    for player in players:
        if other_team != player:
            this_player = player
    if not current_board.is_terminal(this_player):
        if last_move:
            move_option = current_board.move_option(this_player, last_move)
        else:
            move_option = current_board.move_option(this_player)
        random_pos = random.choice(move_option)
        potential_moves = current_board.get_potential_moves(random_pos)
        while len(potential_moves) == 0:
            random_pos = random.choice(current_board.move_option(this_player))
            potential_moves = current_board.get_potential_moves(random_pos)
        
        move = random.choice(potential_moves)
        current_board.make_move(random_pos, move)
        print("-----------------------------------")

        current_board.display_board()
        if current_board.check_elimination(random_pos, move):
            random_player(other_team, current_board, move)

def play_against_mcts(board, mcts, iterations):
    turn = "blue"
    print(board.is_game_over(turn))
    while board.is_game_over(turn) == None:

        print(board.squares)
        print("-------------------------------------------")
        print(board.display_board())

        if turn == "blue":
            print("BLUES turn: ")
            chip_to_move = input("Which chip do you want to move: ")
            print(board.get_potential_moves(chip_to_move))
            to_move = input("Where do you want to move the chip to: ")
            board.make_move(chip_to_move, to_move)
            if board.check_elimination(chip_to_move, to_move) == True:
                turn = "blue"
                continue
            turn = "red"
            print(board.display_board())
        print(board.squares)
        if board.is_game_over(turn) == None:
            if turn == "red":
                print("REDS turn (MCTS): ")
                mcts_board = board.copy()  # Create a copy for MCTSß
                result_state, result_id = mcts.monte_carlo_tree_search(mcts_board, iterations)
                print(result_state, result_id)
                # Apply the best move found by MCTS to the original board
                board.make_move(str(result_state[0]), str(result_state[1]))
                if board.check_elimination(str(result_state[0]), str(result_state[1])) == True:
                    turn = "red"
                    continue
                
                turn = "blue"
    print(board.is_game_over(turn))

    print("Game Over")
    print("-------------------------------------------")
    print("Final Board:")
    print(board.display_board())
    mcts.update_execution_instance()


def play_against_random(board):
    turn = "blue"
    print(board.is_game_over(turn))
    while board.is_game_over(turn) == None:
        print("-------------------------------------------")
        print(board.display_board())

        if turn == "blue":
            print("BLUES turn: ")
            chip_to_move = input("Which chip do you want to move: ")
            to_move = input("Where do you want to move the chip to: ")
            board.make_move(chip_to_move, to_move)
            if board.check_elimination(chip_to_move, to_move) == True:
                turn = "blue"
                continue
            turn = "red"
            print(board.display_board())

        if turn == "red":
            print("REDS turn: ")
            random_player("blue", board)
            turn = "blue"

board = CheckersBoard()
mcts = MCTS_Checkers(board, "test")
time.sleep(3)
play_against_mcts(board, mcts, 200)
time.sleep(3)
