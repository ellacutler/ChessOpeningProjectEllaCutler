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
    def __init__(self, screen_size=(1000, 1000)):
        self.screen = pygame.display.set_mode(screen_size)
        self.incorrect = False
        self.font = pygame.font.SysFont("helveticaneue", 32)
        self.progress_bar_rect = None  # Add this line
        self.try_again_button_rect = None  # add this
        self.next_opening_button_rect = None  # add this

    def draw_text_box(self, text, x, y, width, height):
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)
        return (x, y, width, height)  # return the rect

    def draw_incorrect(self):
        try_again_rect = self.draw_text_box("Try Again", 750, 300, 220, 50)  # make the text box return the rect
        next_opening_rect = self.draw_text_box("Next Opening", 750, 360, 220, 50)
        self.try_again_button_rect = pygame.Rect(try_again_rect)  # create pygame Rect objects
        self.next_opening_button_rect = pygame.Rect(next_opening_rect)


    def draw(self, board, opening=None, game=None):  # added game
        """
        Draws the entire game state to the screen.
        """
        self.screen.fill((200, 200, 150))  # Clear the screen
        self._draw_board()
        self._draw_pieces(board)
        self._draw_ui_elements()
        if opening:
            self._draw_progress_bar(opening) #removed from if incorrect
        if self.incorrect:
            self.draw_incorrect()
        if game:
            self.draw_num_correct(game)
        pygame.display.flip()

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
            piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))  # scale image
            self.screen.blit(piece_image, (PADDING_LEFT + x * SQUARE_SIZE, PADDING_TOP + (7 - y) * SQUARE_SIZE))
        except FileNotFoundError:
            print(f"Warning: Image file for {piece_name} not found.")

    def _draw_ui_elements(self):
        """Draws UI elements like buttons and text boxes."""
        pass

    def _draw_text_box(self, text, x, y, width, height):
        """Draws a text box with the given text."""
        text_surface = self.font.render(text, True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)
        return (x, y, width, height)

    def get_clicked_square(self, mouse_pos):
        """
        Gets the square on the board that was clicked given a mouse position.
        """
        if mouse_pos:
            x, y = mouse_pos
            col = (x - PADDING_LEFT) // SQUARE_SIZE
            row = 7 - ((y - PADDING_TOP) // SQUARE_SIZE)
            if 0 <= col < 8 and 0 <= row < 8:
                # need to convert to chess format -> rank and file
                return (col, row)
            else:
                pass # get buttons 
            
        return None

    def _draw_progress_bar(self, opening):
        """
        Draws a progress bar that shows how far along the user is in the current opening.
        """
        # Constants for the progress bar
        BAR_X = 750
        BAR_Y = 150
        BAR_WIDTH = 200
        BAR_HEIGHT = 30
        BAR_COLOR = (100, 100, 100)
        PROGRESS_COLOR = (0, 255, 0)  # Green for the filled portion

        # Calculate progress
        total_moves = len(opening.moves)
        completed_moves = opening.current_move_index
        if total_moves == 0:
            progress_percentage = 0
        else:
            progress_percentage = completed_moves / total_moves

        progress_width = int(BAR_WIDTH * progress_percentage)
        # Draw the background of the progress bar
        pygame.draw.rect(self.screen, BAR_COLOR, (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT))
        # Draw the progress bar
        pygame.draw.rect(self.screen, PROGRESS_COLOR, (BAR_X, BAR_Y, progress_width, BAR_HEIGHT))

    def draw_num_correct(self, game):
        """
        Draws the number of correct openings that the user has done
        """
        num_correct = game.num_correct
        self.draw_text_box(f"Number Correct: {num_correct}", 750, 100, 220, 30)
