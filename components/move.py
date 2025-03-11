import chess
class Move():
    def __init__(self, **kwargs):
        self.board = kwargs.get("board")  # Board is now optional
        self.start_posn = kwargs.get("start_posn")
        self.end_posn = kwargs.get("end_posn")
        self.chess_move = None

        if self.start_posn and self.end_posn:
            self.chess_move = self.convert_to_chess_from_posn()
        elif "san" in kwargs and self.board is not None:
            self.chess_move = self.convert_to_chess_from_san(kwargs["san"])
            self.start_posn = self.convert_posn_num(chess.square_name(self.chess_move.from_square))
            self.end_posn = self.convert_posn_num(chess.square_name(self.chess_move.to_square))

        elif "chess_move" in kwargs:
            self.chess_move = kwargs["chess_move"]
            if self.board:
                self.start_posn = self.convert_posn_num(chess.square_name(self.chess_move.from_square))
                self.end_posn = self.convert_posn_num(chess.square_name(self.chess_move.to_square))


    def convert_posn_chess(self, *args):
        """
        converts from a screen position to a board position
        """
        _rank = ["a", "b", "c", "d", "e", "f", "g", "h"]
        _file = ["1", "2", "3", "4", "5", "6", "7", "8"]
        
        return _rank[args[0][0]] + _file[args[0][1]]
    
    def convert_posn_num(self, posn: str):
        """
        converts from an Opening position (internal representation) to move representation
        """
        _rank = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        return (_rank[posn[0]], int(posn[1]) - 1)
    
    def convert_to_chess_from_posn(self):
        """
        converts positions into move objects
        """
        self.start_posn, self.end_posn = self.convert_posn_chess(self.start_posn), self.convert_posn_chess(self.end_posn)
        start_square, end_square = chess.parse_square(self.start_posn), chess.parse_square(self.end_posn)
        return chess.Move(start_square, end_square)
    
    
    def convert_to_chess_from_san(self,san):
        """
        converts internal representation to move object
        """
        try:
            return self.board.parse_san(san)
        except ValueError:
            print(f"Invalid SAN move: {san}")
            return None
    
    def __eq__(self, other):
        """
        Checks if this move is equal to another Move
        """
        if isinstance(other, Move):
            return self.chess_move == other.chess_move
        return False
    def get_san(self):
        """
        Gets the Standard Algebraic Notation (SAN) representation of the move.
        """
        if self.board and self.chess_move:
            return self.board.san(self.chess_move)
        return None
        
    

    
    def execute(self,board):

        board.push(self.chess_move)
    def undo(self,board):
        board.pop()