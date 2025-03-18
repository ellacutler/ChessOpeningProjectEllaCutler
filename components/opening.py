from components.move import Move 
from fsrs import Card, Scheduler, Rating
import chess 
import joblib
import datetime
from typing import List
from components.rating_enum import RatingEnum  # Import RatingEnum
import pytz 


DEFAULT_OPENINGS_FILE = "openings.joblib"
USER_DATA_FILE = "openings_data.joblib"


class Opening():
    def __init__(self,sequence:str, end: chess.WHITE | chess.BLACK, scheduler: Scheduler):
        self.card = Card()
        self.scheduler = scheduler # pass in from opening set 
        self.sequence = sequence
        self.current_move_index = 0
        self._board = chess.Board()
        self.moves = self.convert_to_moves(sequence.split("/"))
        self.end = end
        
    def get_due_date(self) -> datetime:
        """
        getter for due date of card associated with opening
        """
        return self.card.due
    
    
    def set_due_date(self, rating_enum: RatingEnum):
        """
        setter of due date associated with opening, 
        called after an opening is completed correctly or incorrectly
        also sets other internal card data (such as card history)
        """
        print(f'Setting Due Date for ${self.sequence}')
        card, review_log = self.scheduler.review_card(self.card, rating_enum.value[1])
        self.card = card
        
    
    
    
    def convert_to_moves(self, move_strings):
        """
        Converts a list of move strings (ie, "e4") into 
        move objects with reference to preceding moves 
        """
        moves = []
        for move_string in move_strings[1:]: #start at 1 to skip the name of the sequence
            m = Move(san=move_string, board=self._board)  # Create a move from SAN
            moves.append(m)
            self._board.push(m.chess_move) #push the move to the board
        self._board.reset() #reset after we are done getting all the moves
        return moves
    
    def __iter__(self):
        return self
    
    def __next__(self): 
        """
        Gets next move in the sequence 
        """
        if self.current_move_index < len(self.moves):
            move = self.moves[self.current_move_index]
            self.current_move_index += 1
            return move
        else:
            raise StopIteration
    
    def get_next_move(self):
        """
        returns next move in the opening sequence
        """
        if self.current_move_index < len(self.moves):
             move = self.moves[self.current_move_index] # may need to be +1?
             return move 
        return None
    
    def move_forward(self):
        """
        moves the opening sequence board forward by one move
        """
        if self.current_move_index < len(self.moves):
            self.make_move(self.moves[self.current_move_index])
            self.current_move_index += 1
    
    
    def check_move(self, move:Move):
        """
        Checks if the move is correct in the opening sequence
        """
        next_move = self.get_next_move()

        if next_move == None:
            return False

        if move == next_move:
            return True
        else:
            return False

    def get_current_board(self):
        """
        returns internal board state
        """
        return self._board

    


    def save_pgn(self, filepath):
        with open(filepath, "w") as f:
            f.write(str(self._board.variation_san(self.moves)))
    def make_move(self, move: Move):
        self._board.push(move.chess_move)
    def add_move_to_sequence(self, move):
        self.moves.append(move)
    def reset_current_index(self):
        self.current_move_index = 0
        self._board.reset()
    
        
        


class OpeningSet():
    """
    container class for opening sequences
    """

    def __init__(self):
        self.load_data()


        
    def load_data(self):
        try:
            # loaded in data also has card structure and card data (openings)
            loaded_data = joblib.load(USER_DATA_FILE)
            self.items = loaded_data.items
            self.scheduler = loaded_data.scheduler
        except:
            self.scheduler = Scheduler()
            f:List[str] = joblib.load(DEFAULT_OPENINGS_FILE)
            self.items: List[Opening] = self.convert_to_openings(openings_list=f)
            
            
    
    def __iter__(self):
        """
        returns iterator of cards that are due in current gameplay session
        """
        return iter(self.get_due_this_session())
    

    
    def __call__(self):
        return list(self.get_due_this_session())
    
    def get_due_this_session(self):
        """
        returns generator all cards (managed by `scheduler`) that are due this working session
        """
        for item in self.items:
             if item.get_due_date() <= datetime.datetime.now(pytz.utc):
                yield item
            
         
        
    def convert_to_openings(self, openings_list:list) -> list:
        
        """
        Converts list of string sequences into an opening, returns `list` object

        Returns:
            list: A list where each element is a list of move strings.
        """
        opening_sequences = []
        for opening in openings_list:
            opening = self.make_opening(opening)
            opening_sequences.append(opening)
        return opening_sequences
    
    def make_opening(self, sequence_info:str) -> Opening:
        """
        from a string defining an opening, creates "Opening" object
        translation between string defining opening and 
        internal "Opening" object handled in "Opening" class
        """
        
        def get_ending():
            sequence_length = len(sequence_info.split("/"))
            return chess.WHITE if sequence_length % 2 == 0 else chess.BLACK


        
        return Opening(sequence_info, get_ending(), self.scheduler)


