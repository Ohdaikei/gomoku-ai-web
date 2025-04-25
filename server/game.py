import random
EMPTY = None
BLACK = "black"
WHITE = "white"

class Game:
    def __init__(self):
        self.board = []
        self.turn = BLACK
        self.winner = None
        self.game_over = False

    def reset(self, turn, board):
        self.turn = turn
        self.board = [row[:] for row in board]
        self.winner = None
        self.game_over = False

    def state(self):
        return (self.turn, [row[:] for row in self.board])
    
    def place(self, x, y):
        if self.board[y][x] is not None or self.game_over:
            return False
        
        self.board[y][x] = self.turn
        if self.check_win(x, y):
            self.game_over = True
            self.winner = self.turn
        self.turn = BLACK if self.turn == WHITE else WHITE
        return True
    
    def get_actions(self):
        return [(x, y) for y, row in enumerate(self.board) for x, cell in enumerate(row) if cell is None]
    
    def rand_move(self):
        actions = self.get_actions()
        return random.choice(actions) if actions else None
    
    def check_win(self, x, y):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        color = self.board[y][x]
        for dx, dy in directions:
            count = 1
            for d in (1, -1):
                nx, ny = x, y
                while True:
                    nx += dx * d
                    ny += dy * d
                    if 0 <= nx < len(self.board) and 0 <= ny < len(self.board) and self.board[ny][nx] == color:
                        count += 1
                    else:
                        break
            if count >= 5:
                return True
        return False