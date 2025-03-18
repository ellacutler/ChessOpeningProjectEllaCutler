import pygame
import chess
from components.screen import Screen
from components.game import Game
from components.opening import OpeningSet, Opening
from components.rating_enum import RatingEnum


def main():
    pygame.init()
    screen_obj = Screen()
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()

    board = chess.Board()
    game = Game(board, screen_obj)
    
    screen_obj.draw(game.board, game.opening, game)

    running = True

    # openings_set = OpeningSet()
    # openings_list = openings_set()  # Get the list of openings from the OpeningSet

    # current_opening_index = 0
    # game.load_opening(openings_list[current_opening_index])  # Load the first opening

    game.start_practice()  # Start in practice mode initially
    print(f"Starting in Practice Mode with opening: {game.opening.sequence}")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked_square = screen_obj.get_clicked_square(mouse_pos)

                if screen_obj.quit_button_rect and screen_obj.quit_button_rect.collidepoint(
                        mouse_pos):  # check if you're colliding with the quit button

                    running = False
                    

                # elif screen_obj.try_again_button_rect and screen_obj.try_again_button_rect.collidepoint(
                #         mouse_pos):  # check if you're colliding with the buttons
                #     game.handle_button_click(RatingEnum.AGAIN)

                # elif screen_obj.next_opening_button_rect and screen_obj.next_opening_button_rect.collidepoint(
                #         mouse_pos):
                #     game.handle_button_click("Next Opening")

                elif screen_obj.easy_button_rect and screen_obj.easy_button_rect.collidepoint(mouse_pos):
                    game.handle_button_click(RatingEnum.EASY)

                elif screen_obj.hard_button_rect and screen_obj.hard_button_rect.collidepoint(mouse_pos):
                    game.handle_button_click(RatingEnum.HARD)

                elif screen_obj.medium_button_rect and screen_obj.medium_button_rect.collidepoint(mouse_pos):
                    game.handle_button_click(RatingEnum.MEDIUM)

                elif screen_obj.again_button_rect and screen_obj.again_button_rect.collidepoint(mouse_pos):
                    game.handle_button_click(RatingEnum.AGAIN)

                else:
                    screen_obj.show_options = False
                    # screen_obj.draw(board, game.opening, game)  # Moved this line here!

                    if clicked_square:
                        game.manage_current_user_move(clicked_square)  # if not colliding, then run the normal code

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # 'n' for next opening
                    # current_opening_index = (current_opening_index + 1) % len(openings_list)
                    # game.board.reset()
                    # game.load_opening(openings_list[current_opening_index])
                    # game.opening.reset_current_index()
                    # print(f"Loaded next opening: {game.opening.sequence}")
                    pass
                if event.key == pygame.K_p:  # 'p' for previous
                    pass
                    # current_opening_index = (current_opening_index - 1) % len(openings_list)
                    # game.board.reset()
                    # game.load_opening(openings_list[current_opening_index].sequence, end=openings_list[current_opening_index].end)
                    # game.opening.reset_current_index()
                    # print(f"Loaded next opening: {game.opening.sequence}")

        # screen_obj.draw(game.board, game.opening, game)


        pygame.display.flip()
        clock.tick(30)
    game.save_cards_data()
    pygame.quit()


if __name__ == "__main__":
    main()
