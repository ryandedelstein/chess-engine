#from chess_game.piece import Pawn, Piece
import copy
from turtle import position

class Board:
    def __init__(self):
        self.fill_board()
        
        #load the intial board

        #add white pawns
        # for i in range(8):
        #     self.positions[i][1] = Pawn(i, 1, 1)
        # #add black pawns
        # for i in range(8):
        #     self.positions[i][6] = Pawn(i, 6, 2)
        
        #add rooks
        # self.positions[0][0] = Rook(0, 0, 1)
        # self.positions[7][0] = Rook(7, 0, 1)

        #add knights
        # self.positions[1][0] = Knight(1,0,1)
        # self.positions[6][0] = Knight(6,0,1)
        # self.positions[1][7] = Knight(1,7,2)
        # self.positions[6][7] = Knight(6,7,2)

        #add bishops
        self.positions[2][0] = Bishop(2,0,1)
        self.positions[5][0] = Bishop(5,0,1)
        self.positions[2][7] = Bishop(2,7,2)
        self.positions[5][7] = Bishop(5,7,2)

        #extra fields
        self.white_king = (4,0)
        self.black_king = (4,7)

        self.white_can_castle = True
        self.black_can_castles = True
        self.print_board()



    def print_board(self):
        b = self.positions
        for i in range(8):
            for j in range(8):
                if b[i][j] is None:
                    print("_", end="  ")
                elif b[i][j].get_color() == 1:
                    print("X", end = "  ")
                else:
                    print("O", end = "  ")
            print()






    def fill_board(self):
        self.positions = []
        for i in range(8):
            curr = []
            for j in range(8):
                curr.append(None)
            self.positions.append(curr)
    
    #returns 0 if empty, 1 if white, 2 if black
    def is_piece(self, x_pos, y_pos):        
        if self.positions[x_pos][y_pos] is None:
            return 0
        else:
            return self.positions[x_pos][y_pos].get_color()
    
    def get_piece(self, pos):
        return self.positions[pos[0]][pos[1]]
    
    def get_white_king(self):
        return self.white_king
    
    def get_black_king(self):
        return self.black_king

    def get_next_move(self, pos, move):
        ret = copy.deepcopy(self)

        x = pos[0] + move[0]
        y = pos[1] + move[1]

        
        new_piece = copy.deepcopy(self.positions[pos[0]][pos[1]])
        #handle when pawn is promoted
        new_piece.update_position(x,y)
        ret.positions[pos[0]][pos[1]] = None
        ret.positions[x][y] = new_piece

        return ret
    
    def white_can_castle(self):
        ret = []
        if self.black_can_castles:

    
    def white_in_check(self):
        black_pieces = self.__get_black_pieces__()
        for i in black_pieces:
            if i.checks_white_king(self):
                return True
        return False

    def black_in_check(self):
        white_pieces = self.__get_white_pieces__()
        for i in white_pieces:
            if i.checks_black_king(self):
                return True
        return False
        
    def __get_black_pieces__(self):
        ret = []
        for i in range(8):
            for j in range(8):
                if self.positions[i][j] is None:
                    continue
                if self.positions[i][j].get_color() == 2:
                    ret.append(self.positions[i][j])
        return ret

    def __get_white_pieces__(self):
        ret = []
        for i in range(8):
            for j in range(8):
                if self.positions[i][j] is None:
                    continue
                if self.positions[i][j].get_color() == 1:
                    ret.append(self.positions[i][j])
        return ret








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
            if possible_moves[0] == (0,1): 
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
            if possible_moves[0] == (0,-1): 
                if board.is_piece(self.x_pos, self.y_pos - 2) == 0:
                    if self.valid_move(board,(0,-2)):
                        possible_moves.append((0,-2))
        
        return possible_moves
    
    def can_capture(self, board, pos, king = False):
        if not king and not self.valid_move(board, (pos[0] - self.x_pos, pos[1] - self.y_pos)):
            return False
        if self.color == 1:
            return self.__white_can_capture__(board, pos)
        return self.__black_can_capture__(board, pos)

    def __white_can_capture__(self, board, pos):
        return pos[1] == self.y_pos + 1 and (pos[0] == self.x_pos - 1 or pos[0] == self.x_pos + 1)
    
    def __black_can_capture__(self, board, pos):
        return pos[1] == self.y_pos - 1 and (pos[0] == self.x_pos - 1 or pos[0] == self.x_pos + 1)

    def checks_white_king(self, board):
        king = board.get_white_king()
        return self.y_pos == king[1] + 1 and (self.x_pos == king[0] - 1 or self.x_pos == king[0] + 1)

    def checks_black_king(self, board):
        king = board.get_black_king()
        return self.y_pos == king[1] - 1 and (self.x_pos == king[0] - 1 or self.x_pos == king[0] + 1)




class Knight(Piece):
    def __init__(self, _x_pos, _y_pos, _color):
        super().__init__(_x_pos, _y_pos, _color)
    
    def get_moves(self, board):
        if self.color == 1:
            return self.__get_moves_white__(board)
        return self.__get_moves_black__(board)

    def __get_moves_white__(self, board):
        possible_moves = []
        tests = [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]
        for i in tests:
            next_x = self.x_pos + i[0]
            next_y = self.y_pos + i[1]
            if next_x > 7 or next_x < 0 or next_y > 7 or next_y < 0:
                continue
            if not board.is_piece(next_x, next_y) == 1:
                if self.valid_move(board, i):
                    possible_moves.append(i)
        
        return possible_moves

    def __get_moves_black__(self, board):
        possible_moves = []
        tests = [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]
        for i in tests:
            next_x = self.x_pos + i[0]
            next_y = self.y_pos + i[1]
            if next_x > 7 or next_x < 0 or next_y > 7 or next_y < 0:
                continue
            if not board.is_piece(next_x, next_y) == 2:
                if self.valid_move(board, i):
                    possible_moves.append(i)
        
        return possible_moves
    
    def can_capture(self, board, pos, king = False):
        if not king and not self.valid_move(board, (pos[0] - self.x_pos, pos[1] - self.y_pos)):
            return False
        if king:
            for i in [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]:
                if (self.x_pos + i[0], self.y_pos + i[1]) == pos:
                    return True
                return False
        moves = self.get_moves(board)
        move = (pos[0]-self.x_pos, pos[1] - self.y_pos)
        return move in moves
    
    def checks_white_king(self, board):
        king = board.get_white_king()
        for i in [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]:
            if (self.x_pos + i[0], self.y_pos + i[1]) == king:
                return True
        return False
    
    def checks_black_king(self, board):
        king = board.get_black_king()
        for i in [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]:
            if (self.x_pos + i[0], self.y_pos + i[1]) == king:
                return True
        return False

class Bishop(Piece):
    def __init__(self, _x_pos, _y_pos, _color):
        super().__init__(_x_pos, _y_pos, _color)
    
    def get_moves(self, board):
        if self.color == 1:
            return self.__get_moves_white__(board)
        return self.__get_moves_black__(board)

    def __get_moves_white__(self, board):
        possible_moves = []
        tests = []
        tests.append([(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)]) 
        tests.append([(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)])
        tests.append([(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)])
        tests.append([(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)])
        for j in tests:
            for i in j:
                next_x = self.x_pos + i[0]
                next_y = self.y_pos + i[1]
                if next_x > 7 or next_x < 0 or next_y > 7 or next_y < 0:
                    break
                if board.is_piece(next_x, next_y) == 1:
                    break
                elif board.is_piece(next_x, next_y) == 2:
                    if self.valid_move(board, i):
                        possible_moves.append(i)
                    break
                else:
                    if self.valid_move(board, i):
                        possible_moves.append(i)
        
        return possible_moves

    def __get_moves_black__(self, board):
        possible_moves = []
        tests = []
        tests.append([(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)]) 
        tests.append([(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)])
        tests.append([(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)])
        tests.append([(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)])
        for j in tests:
            for i in j:
                next_x = self.x_pos + i[0]
                next_y = self.y_pos + i[1]
                if next_x > 7 or next_x < 0 or next_y > 7 or next_y < 0:
                    break
                if board.is_piece(next_x, next_y) == 2:
                    break
                elif board.is_piece(next_x, next_y) == 1:
                    if self.valid_move(board, i):
                        possible_moves.append(i)
                    break
                else:
                    if self.valid_move(board, i):
                        possible_moves.append(i)
        
        return possible_moves
    
    def can_capture(self, board, pos, king = False):
        if not king and not self.valid_move(board, (pos[0] - self.x_pos, pos[1] - self.y_pos)):
            return False
        if king:
            for i in [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]:
                if (self.x_pos + i[0], self.y_pos + i[1]) == pos:
                    return True
                return False
        moves = self.get_moves(board)
        move = (pos[0]-self.x_pos, pos[1] - self.y_pos)
        return move in moves
    
    def checks_white_king(self, board):
        king = board.get_white_king()
        tests = []
        tests.append([(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)]) 
        tests.append([(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)])
        tests.append([(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)])
        tests.append([(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)])
        for j in tests:
            for i in j:
                next_x = self.x_pos + i[0]
                next_y = self.y_pos + i[1]
                if next_x > 7 or next_x < 0 or next_y > 7 or next_y < 0:
                    break
                if (next_x,next_y) == king:
                    return True
                if not board.is_piece(next_x, next_y) == 0:
                    break
                
        
        return False
    
    def checks_black_king(self, board):
        king = board.get_black_king()
        tests = []
        tests.append([(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)]) 
        tests.append([(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)])
        tests.append([(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)])
        tests.append([(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)])
        for j in tests:
            for i in j:
                next_x = self.x_pos + i[0]
                next_y = self.y_pos + i[1]
                if next_x > 7 or next_x < 0 or next_y > 7 or next_y < 0:
                    break
                if (next_x,next_y) == king:
                    return True
                if not board.is_piece(next_x, next_y) == 0:
                    break
                
        
        return False



class Rook(Piece):
    def __init__(self, _x_pos, _y_pos, _color):
        super().__init__(_x_pos, _y_pos, _color)
        self.has_moved = False
    
    def get_moves(self, board):
        if self.color == 1:
            return self.__get_moves_white__(board)
        return self.__get_moves_black__(board)

    def __get_moves_white__(self, board):
        possible_moves = []
        tests = []
        tests.append([(1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0)]) 
        tests.append([(0,-1), (0,-2), (0,-3), (0,-4), (0,-5), (0,-6), (0,-7)])
        tests.append([(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7)])
        tests.append([(-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0)])
        for j in tests:
            for i in j:
                next_x = self.x_pos + i[0]
                next_y = self.y_pos + i[1]
                if next_x > 7 or next_x < 0 or next_y > 7 or next_y < 0:
                    break
                if board.is_piece(next_x, next_y) == 1:
                    break
                elif board.is_piece(next_x, next_y) == 2:
                    if self.valid_move(board, i):
                        possible_moves.append(i)
                    break
                else:
                    if self.valid_move(board, i):
                        possible_moves.append(i)
        
        #check for castling
        #first kingside
        if self.has_moved or not board.white_can_castle:
            return possible_moves

        #kingside
        if self.x_pos == 0:
            if board.is_piece((0,1)) == 0 and board.is_piece((0,2)) == 0:
                test1 = board.
        elif self.y_pos == 7:
            e

        return possible_moves

    def __get_moves_black__(self, board):
        possible_moves = []
        tests = []
        tests.append([(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)]) 
        tests.append([(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)])
        tests.append([(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)])
        tests.append([(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)])
        for j in tests:
            for i in j:
                next_x = self.x_pos + i[0]
                next_y = self.y_pos + i[1]
                if next_x > 7 or next_x < 0 or next_y > 7 or next_y < 0:
                    break
                if board.is_piece(next_x, next_y) == 2:
                    break
                elif board.is_piece(next_x, next_y) == 1:
                    if self.valid_move(board, i):
                        possible_moves.append(i)
                    break
                else:
                    if self.valid_move(board, i):
                        possible_moves.append(i)
        
        return possible_moves
    
    def can_capture(self, board, pos, king = False):
        if not king and not self.valid_move(board, (pos[0] - self.x_pos, pos[1] - self.y_pos)):
            return False
        if king:
            for i in [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]:
                if (self.x_pos + i[0], self.y_pos + i[1]) == pos:
                    return True
                return False
        moves = self.get_moves(board)
        move = (pos[0]-self.x_pos, pos[1] - self.y_pos)
        return move in moves
    
    def checks_white_king(self, board):
        king = board.get_white_king()
        tests = []
        tests.append([(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)]) 
        tests.append([(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)])
        tests.append([(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)])
        tests.append([(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)])
        for j in tests:
            for i in j:
                next_x = self.x_pos + i[0]
                next_y = self.y_pos + i[1]
                if next_x > 7 or next_x < 0 or next_y > 7 or next_y < 0:
                    break
                if (next_x,next_y) == king:
                    return True
                if not board.is_piece(next_x, next_y) == 0:
                    break
                
        
        return False
    
    def checks_black_king(self, board):
        king = board.get_black_king()
        tests = []
        tests.append([(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)]) 
        tests.append([(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)])
        tests.append([(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)])
        tests.append([(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)])
        for j in tests:
            for i in j:
                next_x = self.x_pos + i[0]
                next_y = self.y_pos + i[1]
                if next_x > 7 or next_x < 0 or next_y > 7 or next_y < 0:
                    break
                if (next_x,next_y) == king:
                    return True
                if not board.is_piece(next_x, next_y) == 0:
                    break
                
        
        return False