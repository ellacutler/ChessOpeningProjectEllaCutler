import chess

class Board(chess.Board):

    """
    Responsible for `chess.board()` for each opening
    will eventually convert between my friend's file and chess.board(), I think? created as a placeholder for now
    """
    def __init__(self):
        super().__init__()

    def __call__(self):
        return self
    
    # @property
    # def string_board(self):
        
    #     strcb = str(self)
    #     cb = [line.split() for line in strcb.splitlines()]
    #     return cb 
    
    def reset(self):
        self.reset_board()
