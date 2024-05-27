import math
import random
import uuid
from databasePostgres.dataConnect import Postgres
from datetime import datetime
from helpers import remove_str_list
import json

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
        self.postgres_connect.insert_into_table("Execution", (self.id, self.title, str(self.start_time).split('.')[0], "0", self.title))
        if not self.postgres_connect.check_if_record_exists("Node", "node_id", '0'):
            self.postgres_connect.insert_into_table("Node", ('0', '0', self.id, 1, '0', '0', 0, 0)) 
    
    def update_execution_instance(self):
        end_time = datetime.now()
        self.postgres_connect.update_record("Execution", self.id, {"endtime": str(end_time)}, "exe_id")


    def select(self, node, depth=None):
        exploration_rate = 0.7
        count = 0
        while node.children:
            # Filter out child nodes with zero visits
            non_zero_children = [child for child in node.children if child.visits != 0]

            if non_zero_children and random.random() < exploration_rate:
                # Select a random child to explore
                node = random.choice(node.children)
            else:
                if non_zero_children:
                    # Select the child with the maximum value based on UCB1 formula
                    node = max(non_zero_children, key=lambda child: child.value / child.visits + math.sqrt(2 * math.log(node.visits) / child.visits))
                else:
                    # All children have zero visits, break out of the loop or handle this case as needed
                    break
            count += 1

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
                # if node exists don't create new node treat it as existing with extra visits exetra.
                new_node = Node(new_board, move=[move, p_moves], parent=node)
                self.postgres_connect.insert_into_table("Node", (new_node.id, new_node.get_parent_id(), self.id, new_node.chosen, remove_str_list(new_node.move), remove_str_list(new_node.get_childern_id()), new_node.value, new_node.visits))
                self.postgres_connect.insert_into_table("State_tb", (json.dumps(new_node.state.squares), new_node.id))
                node.children.append(new_node)
                self.postgres_connect.update_record("Node", str(node.id), {"childern": remove_str_list(node.get_childern_id())}, "node_id")
                # check if node exists by move and parent_id
        if node.children:
            return random.choice(node.children)
        else:
            return None

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
        return current_state.get_result("red")  


    def backpropagate(self, node, result):
        while node:
            node.visits += 1
            node.value += result
            self.postgres_connect.update_record("Node", node.id, {"visits": node.visits, "value_": node.value}, "node_id")
            node = node.parent

    def monte_carlo_tree_search(self, initial_state, iterations):
        root = Node(initial_state)
        #insert this node as the parent node with an id of 1 so it can be used as the roort for visualisation set chosen = 1 aswell
        self.postgres_connect.insert_into_table("Node", (root.id, root.parent_id, self.id, 1, remove_str_list(root.move), remove_str_list(root.get_childern_id()), root.value, root.visits))

        for _ in range(iterations):
            selected_node = self.select(root, 1)
            if _ == 1:
                expanded_node = self.expand(selected_node, initial_state)
            else:
                expanded_node = selected_node
            if expanded_node:
                simulation_result = self.simulate(expanded_node)
                self.backpropagate(expanded_node, simulation_result)

        best_child = max(root.children, key=lambda child: child.visits)
        best_child.set_chosen()
        self.postgres_connect.update_record("Node", best_child.id, {"chosen": 1}, "node_id")
        return best_child.move, best_child.id
    

