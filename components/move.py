import chess
class Move():
    def __init__(self, **kwargs):
        self.start_posn = kwargs["start_posn"]
        self.end_posn = kwargs["end_posn"]
        self.board = kwargs["board"]
        # self.piece = kwargs["piece"]
        self.chess_move = self.convert_to_chess()
    
    
    def convert_posn_chess(self, *args):
        _rank = ["a", "b", "c", "d", "e", "f", "g", "h"]
        _file = ["1", "2", "3", "4", "5", "6", "7", "8"]
        
        return _rank[args[0][0]] + _file[args[0][1]]
    
    
    def convert_to_chess(self):
        self.start_posn, self.end_posn = self.convert_posn_chess(self.start_posn), self.convert_posn_chess(self.end_posn)
        start_square, end_square = chess.parse_square(self.start_posn), chess.parse_square(self.end_posn)
        return chess.Move(start_square, end_square)
    
    def valid_move(self,board):
        return board.is_legal(self.chess_move)
    
    def execute(self,board):
        if self.valid_move(board):
            board.push(self.chess_move)
    def undo(self,board):
        board.pop()