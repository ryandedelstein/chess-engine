from chess_game.board import Board

class Piece:
    def __init__(self, _x_pos, _y_pos, _color):
        self.x_pos = _x_pos
        self.y_pos = _y_pos
        self.color = _color
    
    def get_position(self):
        return (self.x_pos, self.y_pos)
    
    def get_color(self):
        return self.color
    
    def update_position(self, _x_pos, _y_pos):
        self.x_pos = _x_pos
        self.y_pos = _y_pos
        return self.get_position()

    def valid_move(self, board, move):
        if self.x_pos + move[0] > 7 or self.x_pos + move[0] < 0:
            return False
        if self.y_pos + move[1] > 7 or self.y_pos + move[1] < 0:
            return False
        if self.color == 1:
            return not board.get_next_move(self.get_position(), move).white_in_check()
        return not board.get_next_move(self.get_position(), move).black_in_check()

class Pawn(Piece):
    def __init__(self, _x_pos, _y_pos, _color):
        super().__init__(_x_pos, _y_pos, _color)
    
    def get_moves(self, board):
        if self.color == 1:
            return self.__get_moves_white__(board)
        return self.__get_moves_black__(board)

    def __get_moves_white__(self, board):
        possible_moves = []
        if self.y_pos == 7:
            return possible_moves
        
        if board.is_piece(self.x_pos, self.y_pos + 1) == 0:
            if self.valid_move(board,(0,1)):
                possible_moves.append((0,1))
        
        if board.is_piece(self.x_pos - 1, self.y_pos + 1) == 2:
            if self.valid_move(board,(-1,1)):
                possible_moves.append((-1,1))

        if board.is_piece(self.x_pos + 1, self.y_pos + 1) == 2:
            if self.valid_move(board,(1,1)):
                possible_moves.append((1,1))
        
        if self.y_pos == 1:
            if possible_moves[0] == (1,1): 
                if board.is_piece(self.x_pos, self.y_pos + 2) == 0:
                    if self.valid_move(board,(0,2)):
                        possible_moves.append((0,2))
        
        return possible_moves

    def __get_moves_black__(self, board):
        possible_moves = []
        if self.y_pos == 0:
            return possible_moves
        
        if board.is_piece(self.x_pos, self.y_pos - 1) == 0:
            if self.valid_move(board,(0,-1)):
                possible_moves.append((0,-1))
        
        if board.is_piece(self.x_pos - 1, self.y_pos - 1) == 1:
            if self.valid_move(board,(-1,-1)):
                possible_moves.append((-1,-1))

        if board.is_piece(self.x_pos + 1, self.y_pos - 1) == 1:
            if self.valid_move(board,(1,-1)):
                possible_moves.append((1,-1))
        
        if self.y_pos == 6:
            if possible_moves[0] == (1,-1): 
                if board.is_piece(self.x_pos, self.y_pos - 2) == 0:
                    if self.valid_move(board,(0,-2)):
                        possible_moves.append((0,-2))
        
        return possible_moves
    
    def can_capture(self, board, pos, king = False):
        if not king and not self.valid_move(board, (pos[0] - self.x_pos, pos[1] - self.y_pos)):
            return False
        if self.color == 1:
            return self.__white_can_capture__(pos)
        return self.__black_can_capture__(pos)

    def __white_can_capture__(self, board, pos):
        return pos[1] == self.y_pos + 1 and (pos[0] == self.x_pos - 1 or pos[0] == self.x_pos + 1)
    
    def __black_can_capture__(self, board, pos):
        return pos[1] == self.y_pos - 1 and (pos[0] == self.x_pos - 1 or pos[0] == self.x_pos + 1)
