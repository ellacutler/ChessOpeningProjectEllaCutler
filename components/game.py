from components.board import Board 
from components.piece import Piece
from components.move import Move 
from components.opening import Opening
import chess


class Game():
    """
    pygame logic that doesn't belong in "main.py"
    """
    def __init__(self, board: Board, history = None):
        self.board : Board = board
        self.history : lst[Move] |None  = history
        self.curr_move = []     
        self.practice_mode = False   

    # need a posn -> move thing here 
    def load_opening(self, opening_name, moves=None):
            self.opening = Opening(opening_name, moves)

    def manage_current_user_move(self, posn):
        if posn and len(self.curr_move) < 2:
            # handle square
            self.curr_move.append(posn)
        if len(self.curr_move) == 2:
            # user clicked move -> decide if it is valid
            m = Move(start_posn = self.curr_move[0], end_posn = self.curr_move[1], board=self.board)
            self.make_user_move(m)
            self.curr_move = []
            

    
    def make_user_move(self, move):
        if self.practice_mode:
            is_correct = self.opening.check_move(move)
            if is_correct:
                self.opening.move_forward()
                return True
            else:
                return False
        else:
            move.execute(self.board)
            return True

    def next_move(self):
        self.opening.move_forward()

    def prev_move(self):
        self.opening.move_backward()
    def start_practice(self):
        self.practice_mode = True
    def change_mode(self):
        self.practice_mode = not self.practice_mode
    def add_move_to_sequence(self, move):
        self.opening.add_move_to_sequence(move)
    def save_opening(self, filepath):
        self.opening.save_pgn(filepath)
    @property
    def pieces(self):
        #returns the pieces for the current board
        pieces = []
        for square in chess.SQUARES:
            piece = self.board.board.piece_at(square)
            if piece:
                pieces.append(piece)
        return pieces
        