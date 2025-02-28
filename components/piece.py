class Piece():
    def __init__(self, **kwargs):
        self.posn = kwargs["posn"]
        self.color = kwargs["color"]
        self.captured = False
    
    def get_moves(self, board):
        pass


class Pawn(Piece): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Rook(Piece): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
class King(Piece):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Queen(Piece):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Knight(Piece):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
class Bishop(Piece):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)