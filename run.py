import pygame
from components.board import Board
from components.screen import Screen
from components.game import Game  

def main():
    pygame.init()
    screen_obj = Screen()
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()

    board = Board()
    game = Game(board) 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # ... handle other events (mouse clicks, etc.)
            curr_move = []
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked_square = screen_obj.get_clicked_square(mouse_pos)
                game.manage_current_user_move(clicked_square)

                    

        screen_obj.screen.fill((0,0,0))
        screen_obj.draw(board)

        pygame.display.flip()
        clock.tick(60) 

    pygame.quit()

if __name__ == "__main__":
    main()
