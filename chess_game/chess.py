from ast import Raise
from board import Board


class Chess:
    def __init__(self):
        self.game = Board()
        self.turn = 1
    
    def play_move(self, pos, move):
        
        piece = self.game.get_piece(pos)
        if not piece:
            raise Exception("No piece on that square")
        if not piece.get_color() == self.turn:
            raise Exception("Piece is wrong color")
        moves = piece.get_moves(self.game)
        print(moves)
        if not move in moves:
            raise Exception("Invalid move")
        
        self.game = self.game.get_next_move(pos, move)
        if self.turn == 1:
            self.turn = 2
        else: 
            self.turn = 1
        
        self.game.print_board()
