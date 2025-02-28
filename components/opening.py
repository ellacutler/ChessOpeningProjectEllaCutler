from components.move import Move 
import chess 


class OpeningSet():
    """
    container class for opening sequences
    """
    pass 
class Opening():
    def __init__(self,sequence:str, moves: list[Move] | None):
        self.sequence = sequence
        # will also want to add review date functionality here 
        self.current_move_index = 0
        self._board = chess.Board()
    
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
        if self.current_move_index < len(self.moves):
             move = self.moves[self.current_move_index] # may need to be +1?
             return move 
        return None
    
    def move_forward(self):
        if self.current_move_index < len(self.moves):
            self.make_move(self.moves[self.current_move_index])
            self.current_move_index += 1


    def get_current_board(self):
        return self._board

    def save_pgn(self, filepath):
        with open(filepath, "w") as f:
            f.write(str(self._board.variation_san(self.moves)))
    def make_move(self, move):
        self._board.push_san(move.get_san())
    def add_move_to_sequence(self, move):
        self.moves.append(move)
    def reset_current_index(self):
        self.current_move_index = 0
    
        
        