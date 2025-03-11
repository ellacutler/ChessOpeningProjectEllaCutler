from components.move import Move 
import chess 
import joblib


class Opening():
    def __init__(self,sequence:str, end: chess.WHITE | chess.BLACK):
        self.sequence = sequence
        # will also want to add review date functionality here 
        self.current_move_index = 0
        self._board = chess.Board()
        
        self.moves = self.convert_to_moves(sequence.split("/"))

        self.end = end
    
    
    
    
    def convert_to_moves(self, move_strings):
        """
        Converts a list of move strings into move objects
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

        
        self.items = self.convert_to_openings(joblib.load("./openings.joblib"))
        print("here")
        
    def __iter__(self):
        return self
    
    def __next__(self):
        pass
    
    def __call__(self):
        return self.items
    
    def convert_to_openings(self, openings_list:list):
        
        
        """
        Converts the pygtrie paths to a list of opening sequences (lists of moves).

        Returns:
            list: A list where each element is a list of move strings.
        """
        opening_sequences = []
        for opening in openings_list:
            opening = self.make_opening(opening)
            opening_sequences.append(opening)
        return opening_sequences
    
    def make_opening(self, sequence_info:str) -> Opening:
        
        def get_ending():
            sequence_length = len(sequence_info.split("/"))
            return chess.WHITE if sequence_length % 2 == 0 else chess.BLACK

            pass
        
        return Opening(sequence_info, get_ending())
        
        print("here")
        pass 

