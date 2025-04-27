from __future__ import absolute_import, division, print_function
from math import sqrt, log
from game import Game, WHITE, BLACK, EMPTY
import copy
import time
import random

# class Node:
#     def __init__(self, state, actions, parent=None):
#         self.state = (state[0], copy.deepcopy(state[1]))
#         self.num_wins = 0
#         self.num_visits = 0
#         self.parent = parent
#         self.children = []
#         self.untried_actions = copy.deepcopy(actions)
#         self.simulator = Game()
#         self.simulator.reset(*state)
#         self.is_terminal = self.simulator.game_over


# BUDGET = 1000

# class AI:
#     # NOTE: modifying this block is not recommended because it affects the random number sequences
#     def __init__(self, state):
#         self.simulator = Game()
#         self.simulator.reset(*state) #using * to unpack the state tuple
#         self.root = Node(state, self.simulator.get_actions())

#     def mcts_search(self):

#         iters = 0
#         action_win_rates = {} 

#         # TODO: Implement the MCTS Loop
#         while(iters < BUDGET):
#             if ((iters + 1) % 100 == 0):
#                 # NOTE: if your terminal driver doesn't support carriage returns you can use: 
#                 # print("{}/{}".format(iters + 1, BUDGET))
#                 print("\riters/budget: {}/{}".format(iters + 1, BUDGET), end="")

#             # TODO: select a node, rollout, and backpropagate
#             node = self.root
#             s = self.select(node)
#             winner = self.rollout(s)
#             self.backpropagate(s, winner)


#             iters += 1
#         print()

#         # Note: Return the best action, and the table of actions and their win values 
#         #   For that we simply need to use best_child and set c=0 as return values
#         _, action, action_win_rates = self.best_child(self.root, 0)

#         return action, action_win_rates

#     def select(self, node):

#         # TODO: select a child node
#         # HINT: you can use 'is_terminal' field in the Node class to check if node is terminal node
#         # NOTE: deterministic_test() requires using c=1 for best_child()

#         while node.is_terminal != True:
#             if node.untried_actions:
#                 return self.expand(node)
#             else:
#                 node, _, _ = self.best_child(node)
        
#         return node

        

#     def expand(self, node):

#         # TODO: add a new child node from an untried action and return this new node

#         if node.untried_actions:
#             action = node.untried_actions.pop(0)
#             self.simulator.reset(*node.state)
#             self.simulator.place(*action)
#             actions = self.simulator.get_actions()
#             state = self.simulator.state()
#             child_node = Node(state, actions, node)
#             node.children.append((action, child_node))
#             return child_node
#         else:
#             return None
#         #choose a child node to grow the search tree

#         # NOTE: passing the deterministic_test() requires popping an action like this
        

#         # NOTE: Make sure to add the new node to node.children
#         # NOTE: You may find the following methods useful:
#         #   self.simulator.state()
#         #   self.simulator.get_actions()

#         return child_node

#     def best_child(self, node, c=1): 

#         # TODO: determine the best child and action by applying the UCB formula
#         best_child_node = None # to store the child node with best UCB
#         best_action = None # to store the action that leads to the best child
#         action_ucb_table = {} # to store the UCB values of each child node (for testing)
#         max_ucb = float('-inf')

#         total_visits = node.num_visits

#         # NOTE: deterministic_test() requires iterating in this order
#         for action, child in node.children:
#             if child.num_visits == 0:
#                 ucb = float('inf')
#             else:
#                 win_rate = child.num_wins / child.num_visits
#                 exploration = c * sqrt((2 * log(total_visits)) / child.num_visits)
#                 ucb = win_rate + exploration

#             action_ucb_table[action] = ucb
#             if ucb > max_ucb:
#                 max_ucb = ucb
#                 best_child_node = child
#                 best_action = action
#             # NOTE: deterministic_test() requires, in the case of a tie, choosing the FIRST action with 
#             # the maximum upper confidence bound 

#         return best_child_node, best_action, action_ucb_table

#     def backpropagate(self, node, result):

#         while (node is not None):
#             # TODO: backpropagate the information about winner
#             # IMPORTANT: each node should store the number of wins for the player of its **parent** node
#             parent_node = node.parent
#             node.num_visits += 1
#             if node.parent is not None:
#                 parent_player = node.parent.state[0]
#                 # print(parent_player)
#                 node.num_wins += result[parent_player]
#             node = parent_node
            

#     def rollout(self, node):

#         # TODO: rollout (called DefaultPolicy in the slides)

#         # HINT: you may find the following methods useful:
#         #   self.simulator.reset(*node.state)
#         #   self.simulator.game_over
#         #   self.simulator.rand_move()
#         #   self.simulator.place(r, c)
#         # NOTE: deterministic_test() requires that you select a random move using self.simulator.rand_move()
#         self.simulator.reset(*node.state)
#         while self.simulator.game_over != True:
#             move = self.simulator.rand_move()
#             self.simulator.place(*move)


#         # Determine reward indicator from result of rollout
#         reward = {}
#         if self.simulator.winner == BLACK:
#             reward[BLACK] = 1
#             reward[WHITE] = 0
#         elif self.simulator.winner == WHITE:
#             reward[BLACK] = 0
#             reward[WHITE] = 1
#         return reward
    
#     # def rollout(self, node):
#     #     self.simulator.reset(*node.state)
#     #     while not self.simulator.game_over:
#     #         current_player = node.state[0]
#     #         move = self.select_move_with_strategy(current_player)
#     #         self.simulator.place(*move)

#     #     return self.evaluate_result()

#     def select_move_with_strategy(self, current_player):
#     # 次の手で勝利できる手を優先
#         actions = self.simulator.get_actions()
#         for action in actions:
#             current_state = self.simulator.state()
#             self.simulator.place(*action)
#             if self.simulator.game_over and self.simulator.winner == current_player:
#                 self.simulator.reset(*current_state)
#                 return action
#             self.simulator.reset(*current_state)
#         return self.simulator.rand_move()
    
#     def evaluate_result(self):
#     # 結果に基づいて評価
#         if self.simulator.winner == BLACK:
#             return {BLACK: 1, WHITE: 0}
#         elif self.simulator.winner == WHITE:
#             return {BLACK: 0, WHITE: 1}
#         else:
#             return {BLACK: 0.5, WHITE: 0.5}
        
class AI:
    def __init__(self, state):
        self.simulator = Game()
        self.simulator.reset(*state)
        self.player_color = state[0]
        self.opponent_color = BLACK if self.player_color == WHITE else WHITE

    def choose_best_move(self):
        actions = self.simulator.get_actions()
        best_score = -float('inf')
        best_action = None

        for x, y in actions:
            score = self.evaluate(x, y)
            if score > best_score:
                best_score = score
                best_action = (x, y)

        if best_action:
            return best_action, best_score
        else:
            return random.choice(actions)
        
    def count_consecutive(self, board, x, y, color):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        max_count = 0
        for dx, dy in directions:
            count = 1
            # 正方向
            nx, ny = x + dx, y + dy
            while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == color:
                count += 1
                nx += dx
                ny += dy
            # 逆方向
            nx, ny = x - dx, y - dy
            while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == color:
                count += 1
                nx -= dx
                ny -= dy
            max_count = max(max_count, count)
        return max_count
    
    def count_total_stones(self, board):
        count = 0
        for row in board:
            for cell in row:
                if cell is not None:
                    count += 1
        return count
    
    def is_near_opponent(self, board, x, y, opponent_color):
        directions = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(board[0]) and 0 <= ny < len(board[1]):
                if board[ny][nx] == opponent_color:
                    return True
        return False


    def evaluate(self, x, y):
        board = self.simulator.board
        board [y][x] = self.player_color
        score = 0

        if self.simulator.check_win(x, y):
            score += 1000000
        else:
            consec = self.count_consecutive(board, x, y, self.player_color)
            if consec == 4:
                score += 7000
            elif consec == 3:
                score += 5000
        board[y][x] = None
        
        self.simulator.board[y][x] = self.opponent_color
        if self.simulator.check_win(x, y):
            score += 90000
        else:
            consec = self.count_consecutive(board, x, y, self.opponent_color)
            if consec == 4:
                score += 8000
            elif consec == 3:
                score += 6000

        board[y][x] = self.player_color
        if self.count_total_stones(board) < 3:
            if self.is_near_opponent(board, x, y, self.player_color):
                score += 1000

        self.simulator.board[y][x] = None

        return score
    

    

