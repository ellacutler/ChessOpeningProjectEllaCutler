import pygame
import chess

if not pygame.get_init():
    pygame.init()

SQUARE_SIZE = 70
PADDING_LEFT = 50
PADDING_TOP = 150
BOARD_COLORS = ["#eeeed2", "#769656"]  
FONT = pygame.font.Font(None, 36)  

class Screen():
    def __init__(self, screen_size = (1000,1000)):
        self.screen = pygame.display.set_mode(screen_size)

    def draw(self, board):
        """
        Draws the entire game state to the screen.
        """
        self.screen.fill((0, 0, 0))  # Clear the screen
        self._draw_board()
        self._draw_pieces(board)
        self._draw_ui_elements()
    
    def __call__(self):
        return self.screen
        

    def _draw_board(self):
        for x in range(8):
            for y in range(8):
                square_color = BOARD_COLORS[(x + y) % 2]
                rect = [PADDING_LEFT + x * SQUARE_SIZE, PADDING_TOP + y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE]
                pygame.draw.rect(self.screen, square_color, rect)

    def _draw_pieces(self, board: chess.Board):
        # board state is *correct* here 
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                x, y = chess.square_file(square), chess.square_rank(square)
                self._draw_piece(piece, x, y)
    def _draw_piece(self, piece: chess.Piece, x, y):


            piece_name = piece.symbol()
            if piece.color:
                # piece.color = True -> white piece
                piece_name = "w" + piece_name
            else:
                # piece.color = False -> black piece
                piece_name = "b" + piece_name.upper()
            

            try:
                
                piece_image = pygame.image.load(f"components/assets/{piece_name}.png")  # Load piece image
                piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE)) #scale image
                self.screen.blit(piece_image, (PADDING_LEFT + x * SQUARE_SIZE, PADDING_TOP + (7-y) * SQUARE_SIZE))
            except FileNotFoundError:
                print(f"Warning: Image file for {piece_name} not found.")
        
    def _draw_ui_elements(self):
        """Draws UI elements like buttons and text boxes."""
        pygame.draw.rect(self.screen, "#eeeed2", [150, 25, 150, 50])  # White button
        pygame.draw.rect(self.screen, "#769656", [500, 25, 150, 50])  # Black button
        pygame.draw.rect(self.screen, "#ADD8E6", [350, 25, 100, 50])  # Add button
        pygame.draw.rect(self.screen, "#ADD8E6", [770, 100, 180, 50])  # Master Moves button
        pygame.draw.rect(self.screen, "#90EE90", [770, 690, 180, 50])  # Show Move button
        pygame.draw.rect(self.screen, "#FFCCCB", [770, 630, 180, 50])  # Practice button
        pygame.draw.rect(self.screen, "#CBC3E3", [770, 570, 180, 50])  # Copy PGN button
        pygame.draw.rect(self.screen, "#f984e5", [770, 510, 180, 50])  # Remove Line button

        self._draw_text_box("White", 150, 25, 150, 50)
        self._draw_text_box("Black", 500, 25, 150, 50)
        self._draw_text_box("Add", 350, 25, 100, 50)
        self._draw_text_box("Master Moves", 770, 100, 180, 50)
        self._draw_text_box("Show Move", 770, 690, 180, 50)
        self._draw_text_box("Practice", 770, 630, 180, 50)
        self._draw_text_box("Copy PGN", 770, 570, 180, 50)
        self._draw_text_box("Remove Line", 770, 510, 180, 50)

    def _draw_text_box(self, text, x, y, width, height):
        """Draws a text box with the given text."""
        text_surface = FONT.render(text, True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)

    def get_clicked_square(self, mouse_pos):
        """
        Gets the square on the board that was clicked given a mouse position.
        """
        if mouse_pos:
            x, y = mouse_pos
            
            col = (x - PADDING_LEFT) // SQUARE_SIZE
            row = 7 - ((y- PADDING_TOP) // SQUARE_SIZE)
            if 0 <= col < 8 and 0 <= row < 8:
                # need to convert to chess format -> rank and file 
                
                return (col,row)
        return None