# -*- coding: utf-8 -*-
import pygame

from constants import WINDOW_CAPTION, FPS
from graphics import make_board_titles, make_menu_buttons, draw_game_screen
from game_engine import (set_up_new_game, handle_events, handle_player_move,
                         make_ai_move)


def main():
    pygame.display.set_caption(WINDOW_CAPTION)
    fps_clock = pygame.time.Clock()

    titles = make_board_titles()
    buttons = make_menu_buttons()
    game_data = set_up_new_game()

    while True:
        game_data, player_move = handle_events(game_data, buttons)

        if player_move and not game_data['game_is_over']:
            game_data = handle_player_move(player_move, game_data)
            if not game_data['game_is_over']:
                game_data = make_ai_move(game_data)

        draw_game_screen(game_data, titles, buttons)
        fps_clock.tick(FPS)


if __name__ == '__main__':
    main()
