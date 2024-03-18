import random
import math
import torch
import torch.nn as nn
import copy



class CheckersBoard:
    def __init__(self):
        self.board_width = 8
        self.board_height = 8
        self.rows = [1,2,3,4,5,6,7,8]
        self.RESET = "\033[0m"
        self.RED = "\033[91m"
        self.BLUE = "\033[94m"
        self.squares = {
            "11": False,
            "21": "blue",
            "31": False,
            "41": "blue",
            "51": False,
            "61": "blue",
            "71": False,
            "81": "blue",
            "12": "blue",
            "22": False,
            "32": "blue",
            "42": False,
            "52": "blue",
            "62": False,
            "72": "blue",
            "82": False,
            "13": False,
            "23": "blue",
            "33": False,
            "43": "blue",
            "53": False,
            "63": "blue",
            "73": False,
            "83": "blue",
            "14": False,
            "24": False,
            "34": False,
            "44": False,
            "54": False,
            "64": False,
            "74": False,
            "84": False,
            "15": False,
            "25": False,
            "35": False,
            "45": False,
            "55": False,
            "65": False,
            "75": False,
            "85": False,
            "16": "red",
            "26": False,
            "36": "red",
            "46": False,
            "56": "red",
            "66": False,
            "76": "red",
            "86": False,
            "17": False,
            "27": "red",
            "37": False,
            "47": "red",
            "57": False,
            "67": "red",
            "77": False,
            "87": "red",
            "18": "red",
            "28": False,
            "38": "red",
            "48": False,
            "58": "red",
            "68": False,
            "78": "red",
            "88": False,

        }
        self.max_width = max(len(str(key)) for key in self.squares.keys())

    def get_colour(self, position):
        for k,v in self.squares.items():
            if k == position:
                return v
    
    def check_bad_moves(self, moves):
        cleaned_moves = []
        for move in moves:
            str_move = str(move)
            if 10 < int(move) < 100 and str_move[0] != "9" and str_move[1] != "9" and not self.squares.get(str_move, True):
                cleaned_moves.append(move)
        return cleaned_moves

    
    def check_can_jump(self, colour):
        all_chips = self.get_all_pos(colour) + self.get_all_pos("K" + colour)
        can_jump = []
        for chips in all_chips:
            colour = self.get_colour(chips)
            if colour == "red" or colour == "Kblue" or colour == "Kred":
                double1 = self.check_double_move(chips, str(int(chips)-11))
                double2 = self.check_double_move(chips, str(int(chips)+9))
                if double1 or double2:
                    can_jump.append(chips)
            if colour == "blue" or colour == "Kblue" or colour == "Kred":
                double1 = self.check_double_move(chips, str(int(chips)+11))
                double2 = self.check_double_move(chips, str(int(chips)-9))
                if double1 or double2:
                    can_jump.append(chips)

        return can_jump

    def pos_double_jump(self, position):
        colour = self.get_colour(position)
        potential_moves = []
        if colour == "blue" or colour == "Kred" or colour == "Kblue":
            double1 = self.check_double_move(position, str(int(position)+11))
            double2 = self.check_double_move(position, str(int(position)-9))
            if double1 != False:
                potential_moves.append(double1)
            if double2 != False:
                potential_moves.append(double2)
        if colour == "red" or colour == "Kblue" or colour == "Kred":
            double1 = self.check_double_move(position, str(int(position)-11))
            double2 = self.check_double_move(position, str(int(position)+9))
            if double1 != False:
                potential_moves.append(double1)
            if double2 != False:
                potential_moves.append(double2)
        return self.check_bad_moves(potential_moves)

    def check_double_move(self, initial_pos, new_pos):
        initial_colour = self.get_colour(initial_pos)
        new_colour = self.get_colour(new_pos)
        if new_colour != False and new_colour != initial_colour and new_colour != None:
            if new_colour[1:] != initial_colour and initial_colour[1:] != new_colour:
                move_dir = int(new_pos) - int(initial_pos) 
                return (str(int(new_pos) + move_dir))
        return False
    
    # FIXME: optimise this
    def get_potential_moves(self, position):
        colour = self.get_colour(position)
        potential_moves = []
        double_moves = []
        if colour == "blue" or colour == "Kred" or colour == "Kblue":
            double1 = self.check_double_move(position, str(int(position)+11))
            double2 = self.check_double_move(position, str(int(position)-9))
            if double1 != False:
                try:
                    double1 = self.check_bad_moves([double1])[0]
                    double_moves.append(double1)
                except Exception as e:
                        if colour[0] != "K":
                            double1 = False
                        pass
            if double2 != False:
                try:
                    double2 = self.check_bad_moves([double2])[0]
                    double_moves.append(double2)
                except Exception as e:
                        if colour[0] != "K":
                            double2 = False
                        pass
        if colour == "red" or colour == "Kblue" or colour == "Kred":
            double1 = self.check_double_move(position, str(int(position)-11))
            double2 = self.check_double_move(position, str(int(position)+9))
            if double1 != False:
                try:
                    double1 = self.check_bad_moves([double1])[0]
                    double_moves.append(double1)
                except Exception as e:
                        if colour[0] != "K":
                            double1 = False
                        pass
            if double2 != False:
                try:
                    double2 = self.check_bad_moves([double2])[0]
                    double_moves.append(double2)
                except Exception as e:
                        if colour[0] != "K":
                            double2 = False
                        pass
        if colour == "blue" or colour == "Kred" or colour == "Kblue":
            if len(double_moves) == 0:
                potential_moves.append(int(position) + 11)
                potential_moves.append(int(position) - 9)
        if colour == "red" or colour == "Kblue" or colour == "Kred":
            if len(double_moves) == 0:
                potential_moves.append(int(position) + 9)
                potential_moves.append(int(position) - 11)
        if len(double_moves) > 0:
            return self.check_bad_moves(double_moves)
        
        return self.check_bad_moves(potential_moves)
    
    def display_board(self):
        board_str = ""
        count = 0
        for k, v in self.squares.items():
            if v == False:
                char = k.ljust(self.max_width + 5)
                board_str += char
            elif v == "blue":
                board_str += self.BLUE + (k.ljust(self.max_width + 5)).upper() + self.RESET
            elif v == "red":
                board_str += self.RED + (k.ljust(self.max_width + 5)).upper() + self.RESET
            elif v == "Kblue":
                board_str += self.BLUE + "K" + (k.ljust(self.max_width + 5)).upper() + self.RESET
            elif v == "Kred":
                board_str += self.RED + "K" + (k.ljust(self.max_width + 5)).upper() + self.RESET
            count += 1
            if count == 8:
                board_str += "\n"
                count = 0
        return board_str
    
    def get_all_pos(self, colour):
        all_pos = []
        for k, v in self.squares.items():
            if v == colour:
                all_pos.append(k)
        return all_pos
    
    
    def make_move(self, position, move):
        colour = self.get_colour(position)
        legal_moves = self.get_potential_moves(position)
        for legal in legal_moves:
            if str(move) == str(legal):
                self.squares[position] = False
                self.squares[str(move)] = colour
                self.turn_to_king(str(move))
                return f"Move {position} to {move} made."
        
        return f"Move {position} to {move} is not a valid move."
    
    def check_elimination(self, initial_pos, new_pos):
        position_moved = int(initial_pos) - int(new_pos)
        if abs(position_moved) == 18 or abs(position_moved) == 22:
            pos_to_eliminate = int(initial_pos) - (position_moved // 2)
            self.squares[str(pos_to_eliminate)] = False
            if len(self.get_potential_moves(new_pos)) > 0 and len(self.pos_double_jump(new_pos)) > 0:
                return True
        return False
    

    def turn_to_king(self, position):
        position = str(position)
        colour = self.get_colour(position)
        if colour == "blue" and position[1] == "8":
            self.squares[position] = "Kblue"
        if colour == "red" and position[1] == "1":
            self.squares[position] = "Kred"

    def check_board(self):
        for k,v in self.squares.items():
            if v == "blue":
                if k[1] != "1":
                    if self.squares[k[0] + str(int(k[1])-1)] == "red":
                        self.squares[k] = False
                        return True
            if v == "red":
                if k[1] != "8":
                    if self.squares[k[0] + str(int(k[1])+1)] == "blue":
                        self.squares[k] = False
                        return True
        return False
    
    def is_game_over(self, colour):
        red = False
        blue = False
        for k,v in self.squares.items():
            if v == "red" or v == "Kred":
                red = True
            if v == "blue" or v == "Kblue":
                blue = True
        if red == True and blue == False:
            return 0
        if blue == True and red == False:
            return 1
        if self.is_stale_mate(colour) == True:
            return 2
    
    def no_moves(self, colour):
        if colour == "blue":
            other_colour = "red"
        else:
            other_colour = "blue"
        for pos in self.get_all_pos(colour) + self.get_all_pos("K" + colour):
            if len(self.get_potential_moves(pos)) > 0:
                for other_pos in self.get_all_pos(other_colour) + self.get_all_pos("K" + other_colour):
                    if len(self.get_potential_moves(other_pos)) > 0:
                        return False
        return True
    
    def is_stale_mate(self, colour):
        stale_mate = True
        if self.no_moves(colour) == True:
            return True
        for k,v in self.squares.items():
            if v == "blue" or v == "red":
                stale_mate = False
        if stale_mate == True:
            return True
         
        
    def copy(self):
        return copy.deepcopy(self)
    
    def is_terminal(self, colour):
        game_status = self.is_game_over(colour)
        if game_status == 0 or game_status == 1 or game_status == 2:
            return True
        return False
    
    def get_result(self, player):
        if player == "blue":
            if self.is_game_over(player) == 1:
                return 1
        if player == "red":
            if self.is_game_over(player) == 0:
                return 1
        
        if self.is_game_over(player) == 2:
            return 0
        return -1
    
    
    def move_option(self, colour, last_move=None):
        all_team = self.get_all_pos(colour) + self.get_all_pos("K" + colour)
        valid_moves = []
        can_jump = self.check_can_jump(colour)
        if last_move:
            if len(self.pos_double_jump(last_move)) > 0:
                valid_moves.append(last_move)
                return valid_moves
        if len(can_jump) > 0:
            for pos in can_jump:
                if len(self.pos_double_jump(pos)) > 0:
                    valid_moves.append(pos)
        if len(valid_moves) == 0:
            for pos in all_team:
                if len(self.get_potential_moves(pos)) > 0:
                    valid_moves.append(pos)
        
        return valid_moves
            