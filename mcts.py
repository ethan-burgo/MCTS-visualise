import math
import random
import uuid
from databasePostgres.dataConnect import Postgres
from datetime import datetime
from helpers import remove_str_list

class Node:
    def __init__(self, state, move=0, parent=0):
        self.state = state
        self.children = []
        self.visits = 0
        self.value = 0
        self.parent = parent
        self.move = move
        self.id = str(uuid.uuid4())[:8]
        self.parent_id = self.get_parent_id()
        self.chosen = 0

    def set_chosen(self):
        self.chosen = 1
    def get_state(self):
        return self.state
    
    def get_id(self):
        return self.id
    
    def get_parent_id(self):
        if self.parent:
            return self.parent.get_id()
        return 0
    def insert_baseline(self):
        pass

    def get_childern_id(self):
        children_id = []
        if len(self.children) > 0:
            for child in self.children:
                children_id.append(str(child.id))
        return children_id

class MCTS_Checkers:
    def __init__(self, board, title):
        self.board = board
        self.title = title
        self.start_time = datetime.now()
        self.postgres_connect = Postgres()
        self.id = str(uuid.uuid4())[:8]
        self.create_execution_instance()

    def create_execution_instance(self):
        self.postgres_connect.insert_into_table("Execution", (self.id, self.title, str(self.start_time).split('.')[0], "0", "test"))
    
    def update_execution_instance(self):
        end_time = datetime.now()
        self.postgres_connect.update_record("Execution", self.id, {"endtime": str(end_time)})

        
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
        #TODO: insert new node?
        moves = new_board.move_option("red")
        for move in moves:
            potential_moves = board.get_potential_moves(move)
            for p_moves in potential_moves:
                new_board = board.copy()
                new_board.make_move(move, p_moves)
                new_board.check_elimination(move, p_moves)
                new_node = Node(new_board, move=[move, p_moves], parent=node)
                print(move)
                self.postgres_connect.insert_into_table("Node", (new_node.id, new_node.get_parent_id(), self.id, new_node.chosen, remove_str_list(new_node.move), remove_str_list(new_node.get_childern_id()), new_node.value, new_node.visits))

                # insert state records
                node.children.append(new_node)
                self.postgres_connect.update_record("Node", str(node.id), {"childern": remove_str_list(node.get_childern_id())})
                #update node with childern values

        if node.children:
            return random.choice(node.children)
        else:
            return None


    # change this to play against a random player
    def simulate(self, node):
        current_state = node.state.copy()  # Create a copy to avoid modifying the original state
        turn = "blue"
        last_move = None
        
        while not current_state.is_terminal("red"):
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
            self.postgres_connect.update_record("Node", node.id, {"visits": node.visits, "value_": node.value})
            node = node.parent

    def monte_carlo_tree_search(self, initial_state, iterations):
        root = Node(initial_state)
        #print(self.id)
        self.postgres_connect.insert_into_table("Node", (root.id, root.get_parent_id(), self.id, root.chosen, remove_str_list(root.move), remove_str_list(root.get_childern_id()), root.value, root.visits))

        for _ in range(iterations):
            selected_node = self.select(root)
            expanded_node = self.expand(selected_node, initial_state)
            if expanded_node:
                simulation_result = self.simulate(expanded_node)
                self.backpropagate(expanded_node, simulation_result)

        best_child = max(root.children, key=lambda child: child.visits)
        best_child.set_chosen()
        print(best_child.get_id(), best_child.move, best_child.chosen)
        self.postgres_connect.update_record("Node", best_child.id, {"chosen": 1})
        return best_child.move

