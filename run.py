import pygame
import chess 
# from components.board import Board
from components.screen import Screen
from components.game import Game
from components.opening import OpeningSet, Opening


def main():
    pygame.init()
    screen_obj = Screen()
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()

    board = chess.Board()
    game = Game(board, screen_obj)

    running = True

    openings_set = OpeningSet()
    openings_list = openings_set()  # Get the list of openings from the OpeningSet

    current_opening_index = 0
    game.load_opening(openings_list[current_opening_index])  # Load the first opening

    game.start_practice()  # Start in practice mode initially
    print(f"Starting in Practice Mode with opening: {game.opening.sequence}")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked_square = screen_obj.get_clicked_square(mouse_pos)
                if screen_obj.try_again_button_rect and screen_obj.try_again_button_rect.collidepoint(mouse_pos): #check if you're colliding with the buttons
                    game.reset_opening_state()
                elif screen_obj.next_opening_button_rect and screen_obj.next_opening_button_rect.collidepoint(mouse_pos):
                    current_opening_index = (current_opening_index + 1) % len(openings_list)
                    game.board.reset()
                    game.load_opening(openings_list[current_opening_index])
                    game.opening.reset_current_index()
                    print(f"Loaded next opening: {game.opening.sequence}")
                else:
                    game.manage_current_user_move(clicked_square) #if not colliding, then run the normal code



                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # 'n' for next opening
                    current_opening_index = (current_opening_index + 1) % len(openings_list)
                    game.board.reset()
                    game.load_opening(openings_list[current_opening_index]) 
                    game.opening.reset_current_index()
                    print(f"Loaded next opening: {game.opening.sequence}")
                if event.key == pygame.K_p: # 'p' for previous
                  current_opening_index = (current_opening_index - 1) % len(openings_list)
                  game.board.reset()
                  game.load_opening(openings_list[current_opening_index].sequence, end= openings_list[current_opening_index].end)
                  game.opening.reset_current_index()
                  print(f"Loaded next opening: {game.opening.sequence}")

        screen_obj.screen.fill((0, 0, 0))
        screen_obj.draw(board)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
