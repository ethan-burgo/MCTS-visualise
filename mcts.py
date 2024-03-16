import math
import random

class Node:
    def __init__(self, state, move=None, parent=None):
        self.state = state
        self.children = []
        self.visits = 0
        self.value = 0
        self.parent = parent
        self.move = move
    
    def get_state(self):
        return self.state

class MCTS_Checkers:
    def __init__(self, board):
        self.board = board
        
    def select(self, node):
        while node.children:
            # Filter out child nodes with zero visits
            non_zero_children = [child for child in node.children if child.visits != 0]

            if non_zero_children:
                # Select the child with the maximum value based on UCB1 formula
                node = max(non_zero_children, key=lambda child: child.value / child.visits + math.sqrt(2 * math.log(node.visits) / child.visits))
            else:
                # All children have zero visits, break out of the loop or handle this case as needed
                break

        return node

    def expand(self, node, board):
        new_board = node.state
        moves = new_board.move_option("red")

        for move in moves:
            potential_moves = board.get_potential_moves(move)
            for p_moves in potential_moves:
                new_board = board.copy()
                new_board.make_move(move, p_moves)
                new_board.check_elimination(move, p_moves)
                new_node = Node(new_board, move=[move, p_moves], parent=node)
                node.children.append(new_node)

        if node.children:
            return random.choice(node.children)
        else:
            return None

    def get_best_move(self, original_board, mcts_result):
        root_node = Node(original_board)  # Create a new root node for the original board
        print(mcts_result)
        root_node.children = mcts_result.children  # Set the children of the root node to the MCTS result children

        # Find the child with the highest number of visits
        best_child = max(root_node.children, key=lambda child: child.visits)
        print(best_child)

        return best_child.move  # The move attribute represents the best move



    # change this to play against a random player
    def simulate(self, node):
        current_state = node.state.copy()  # Create a copy to avoid modifying the original state
        turn = "blue"
        last_move = None
        while not current_state.is_terminal("red"):
            #print("cool")
            #print(current_state.display_board())
            if last_move:
                potential_moves = current_state.move_option(turn, last_move)
            else:
                potential_moves = current_state.move_option(turn)
            last_move = None
            if potential_moves:
                random_pos = random.choice(potential_moves)
                moves = current_state.get_potential_moves(random_pos)

                if moves:
                    random_move = random.choice(moves)
                    current_state.make_move(random_pos, random_move)
                    if current_state.check_elimination(random_pos, random_move):
                        last_move = random_move
                        continue
                    else:
                        if turn == "red":
                            turn = "blue"
                        else:
                            turn = "red"
        #print(current_state.get_result("red"))
        return current_state.get_result("red")  # Return the final result after the playout

    # Implement this function

    def backpropagate(self, node, result):
        while node:
            node.visits += 1
            node.value += result
            node = node.parent

    def monte_carlo_tree_search(self, initial_state, iterations):
        root = Node(initial_state)

        for _ in range(iterations):
            selected_node = self.select(root)
            expanded_node = self.expand(selected_node, initial_state)
            if expanded_node:
                simulation_result = self.simulate(expanded_node)
                self.backpropagate(expanded_node, simulation_result)

        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.move