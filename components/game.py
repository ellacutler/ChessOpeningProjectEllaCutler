from components.board import Board 
from components.piece import Piece
from components.move import Move 
from components.opening import Opening
from components.screen import Screen
import pygame
import chess


class Game():
    """
    pygame logic that doesn't belong in "main.py"
    """
    def __init__(self, board: chess.Board, screen: Screen,  history = None):
        self.board : chess.Board = board
        self.history : lst[Move] |None  = history
        self.curr_move = []     
        self.practice_mode = False   
        self.screen = screen
        self.num_correct = 0 

    # need a posn -> move thing here 
    def load_opening(self, opening:Opening):
        self.opening = opening

    def manage_current_user_move(self, posn):
        """
        event handler for user moves 
        """
        self.screen.draw(self.board, self.opening, self)
        self.screen.incorrect = False
        if posn and len(self.curr_move) < 2:
            # handle square
            self.curr_move.append(posn)
        if len(self.curr_move) == 2:
            # user clicked move -> decide if it is valid
            m = Move(start_posn = self.curr_move[0], end_posn = self.curr_move[1], board=self.board)
            correct = self.make_user_move(m)
            if correct:
                if self.opening.get_next_move():
                    self.make_trainer_move()
                else:
                    self.complete_opening()
                
            else:
                self.screen.incorrect = True
                self.reset_opening_state()
                self.screen.draw(self.board, self.opening, self)


                print("here")
                

            self.curr_move = []
        self.screen.draw(self.board, self.opening, self)

            

    def complete_opening(self):
        """
        handles state after opening is complete 
        """
        self.reset_opening_state()
        self.num_correct += 1 
        
    
    def reset_opening_state(self):
        """
        handles state after opening is reset 
        """
        self.opening.reset_current_index()
        self.board.reset_board()
        
    
    def make_user_move(self, move:Move):
        """
        makes user move 
        """
        if self.practice_mode:
            is_correct = self.opening.check_move(move)
            if is_correct:
                 if self.board.is_legal(move.chess_move): 
                    self.opening.move_forward()
                    move.execute(self.board)
                    return True
                 else:
                    return False
            else:
                return False
        else:
            if self.board.is_legal(move.chess_move): 
                move.execute(self.board)
                return True
            else:
                return False
    
    def make_trainer_move(self):
        next_move = self.opening.get_next_move()
        if next_move:
            if self.board.is_legal(next_move.chess_move):
                self.opening.move_forward()
                next_move.execute(self.board)
        
        

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
            piece = self.board.piece_at(square)
            if piece:
                pieces.append(piece)
        return pieces
        