from components.board import Board 
from components.move import Move 
from components.opening import Opening, OpeningSet
from components.screen import Screen
import pygame
import chess
import time 
import joblib
from typing import List 
from fsrs import Rating

from components.rating_enum import RatingEnum

class Game():
    """
    Game manager, which manages interactions between the screen and the high-level game logic
    """
    def __init__(self, board: chess.Board, screen: Screen):
        self.board : chess.Board = board
        self.curr_move = []     
        self.screen = screen
        self.num_correct = 0 
        self.current_opening_index = 0
        
        try:
            self.openings_list = joblib.load("openings_data.joblib")
        except:
            self.openings_list = OpeningSet()
            
            
        self.load_opening(self.openings_list()[0])
        
    
    def handle_button_click(self, button_type:RatingEnum):
        """
        After a user selects a rating for their opening ("Try again", "easy", "hard", etc.), manages game state with new opening.
        """
        assert type(button_type) is RatingEnum

        self.opening.set_due_date(button_type)
        # move on to next card 
        
        self.reset_opening_state()
        self.load_next_opening()
        print(f'Loaded next opening, ${self.opening.sequence}')


      
        self.screen.show_options = False
        self.screen.incorrect = False # NTS - can get rid of the combo there 
        print(f'Removing Options View and Redrawing Screen')
        self.screen.draw(self.board, self.opening, self)
        
        print(f'Resetting Move List Counter from ${self.curr_move} to ${[]}.')
        self.curr_move = []



    
    
    def save_cards_data(self):
        """
        After user selects "quit", saves practice state data to file. 
        """
        joblib.dump(self.openings_list, "openings_data.joblib")
        print("Saved opening data to `openings_data.joblib`")
    
    # need a posn -> move thing here 
    def load_opening(self, opening:Opening):
        """
        Loads the next opening in the practice sequence into the game, and resets the game state board. 
        """
        print(f'Loading opening, ${opening.sequence}')
        self.opening = opening
        self.opening.reset_current_index()
        self.board = chess.Board()

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
            self.curr_move = []
            if correct:
                if self.opening.get_next_move():
                    
                    self.make_trainer_move()
                     
                else:
                    print(f'Completed Opening: Showing Options')
                    self.screen.show_options = True 
                    
                    self.screen.draw(self.board, self.opening, self)
                    print(f'Showing Options (finished), Reset Current Move to ${[]}')
                    self.reset_opening_state()
                    self.screen.incorrect = False
         #            self.complete_opening()
                
            else:
                self.screen.incorrect = True
#                 self.reset_opening_state()
                self.screen.draw(self.board, self.opening, self)
                print(f'Showing Options (incorrect), Reset Current Move to ${[]}')
                self.reset_opening_state()


                print("here")
        self.screen.draw(self.board, self.opening, self)

            

    def complete_opening(self):
        """
        handles state after opening is complete 
        """
        self.reset_opening_state()
        # load new opening here 
        self.num_correct += 1 
        self.current_opening_index += 1 
        
        try:
            self.load_next_opening()
        except:
            print("Congrats! You have studied all openings for today.")
        
    def load_next_opening(self):
        """
        Identifies the next opening in the practice sequence
        """
        self.reset_opening_state()
        # load new opening here 
        # self.current_opening_index += 1 # i suspect this can and will cause problems 
        self.load_opening(self.openings_list()[0]) # load next one that IS DUE 
        # self.load_opening(self.openings_list[self.current_opening_index])
        

        
    
    def reset_opening_state(self):
        """
        handles state after opening is reset 
        """
        print(f'Resetting self.curr_move from ${self.curr_move} to ${[]}')
        self.curr_move  = []
        
        
        
        self.opening.reset_current_index()
        print(f'Resetting Current Board')
        self.board.reset_board()
        
    
    def make_user_move(self, move:Move):
        """
        makes user move 
        """
        is_correct = self.opening.check_move(move)
        if is_correct:
                self.opening.move_forward()
                if self.board.is_legal(move.chess_move): 
                    # self.opening.move_forward()
                    move.execute(self.board)
                    self.screen.draw(self.board, self.opening, self)
                    return True
                else:
                    return False
        else:
            return False
    
    def make_trainer_move(self) -> None:
        """
        Makes the next move in the sequence, from the chess bot
        Waits in between rendering to simulate actual play
        """
        next_move = self.opening.get_next_move()
        if next_move:
            
            if self.board.is_legal(next_move.chess_move):
                
                self.opening.move_forward()
                self.screen.draw(self.board, self.opening, self)
                time.sleep(0.75) 
                
                next_move.execute(self.board)
                self.screen.draw(self.board, self.opening, self)
        
        
    def next_move(self):
        """
        Iterates the opening forward by 1 move.
        """
        self.opening.move_forward()



