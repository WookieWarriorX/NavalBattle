# -*- coding: utf-8 -*-
import sys
from typing import Optional

import pygame
from pygame import QUIT, KEYUP, K_ESCAPE, MOUSEBUTTONUP

from ai import set_up_ai, get_ai_move
from board_generator import get_random_board
from constants import (
    GameDataType, GameBoardType, TileDataType, TextSurfaceType,
    PLAYER_BOARD_TOPLEFT, ENEMY_BOARD_TOPLEFT,
    STARTGAME_TEXT, MESSAGE_TOPLEFT, ENDGAME_DEFEAT_TEXT, ENDGAME_WIN_TEXT,
    BOARD_WIDTH_IN_PIXELS, BOARD_HEIGHT_IN_PIXELS, GRID_STEP)
from graphics import make_text_surface


def set_up_new_game() -> GameDataType:
    """
    Creates a TypedDict of new game state variables: player and enemy
    boards, AI data, flags and other special variables.

    :return: A TypedDict of game state variables.
    """
    player_board = get_random_board(PLAYER_BOARD_TOPLEFT)
    enemy_board = get_random_board(ENEMY_BOARD_TOPLEFT)
    ai_data = set_up_ai()
    screen_message = make_text_surface(text=STARTGAME_TEXT,
                                       topleft=MESSAGE_TOPLEFT)
    enemy_is_hidden = True
    game_is_over = False

    game_data: GameDataType
    game_data = {'game_is_over': game_is_over,
                 'enemy_is_hidden': enemy_is_hidden,
                 'screen_message': screen_message,
                 'player_board': player_board,
                 'enemy_board': enemy_board,
                 'ai_data': ai_data,
                 'last_ai_move': None,
                 'mouse_position_tile': None}
    return game_data


def get_reference_to_tile(tile_coords: tuple[int, int],
                          board: GameBoardType) -> TileDataType:
    """
    Returns a reference to the given tile from the given board.

    :param tile_coords: Board coordinates of the desired tile
    in (x, y) format.
    :param board: A game board to search the tile.
    :return: A reference to tile information of TileDataType.
    """
    tile_x, tile_y = tile_coords
    link_to_tile = board['tiles'][tile_x][tile_y]
    return link_to_tile


def update_highlighted_tile(current_tile_coords: Optional[tuple[int, int]],
                            last_tile_coords: Optional[tuple[int, int]],
                            board: GameBoardType
                            ) -> GameBoardType:
    """
    Changes highlighted tile on the given board.

    :param last_tile_coords: Coordinates of the last highlighted
    tile in (x, y) format, if any.
    :param current_tile_coords: Coordinates of the current tile
    to highlight, if any, in (x, y) format.
    :param board: The board which a tile is to be highlighted.
    :return: The game board with updated highlighted tile.
    """
    tile_changed = not (current_tile_coords == last_tile_coords)

    if tile_changed:
        if last_tile_coords is not None:
            last_tile = get_reference_to_tile(last_tile_coords, board)
            last_tile['is_lighted'] = False

        if current_tile_coords is not None:
            current_tile = get_reference_to_tile(current_tile_coords, board)
            current_tile['is_lighted'] = True
    return board


def get_tile_at_pixel(pixel_coords: tuple[int, int],
                      board: GameBoardType) -> Optional[tuple[int, int]]:
    """
    Returns board coordinates of a tile at the given pixel coordinates,
    if it exists.

    :param pixel_coords: A tuple of poxel coordinates in (x, y) format.
    :param board: A game board to search the tile.
    :return: A tuple of tile coordinates in (x, y) format if tile
    exists at the given pixel, else None.
    """
    pixel_x, pixel_y = pixel_coords
    x_margin = board['topleft']['pixel_x']
    y_margin = board['topleft']['pixel_y']

    mouse_is_on_board = (
            x_margin < pixel_x < x_margin + BOARD_WIDTH_IN_PIXELS
            and y_margin < pixel_y < y_margin + BOARD_HEIGHT_IN_PIXELS)

    if mouse_is_on_board:
        board_x = (pixel_x - x_margin) // GRID_STEP
        board_y = (pixel_y - y_margin) // GRID_STEP
        return board_x, board_y
    else:
        return None


def get_mouse_position(board: GameBoardType) -> Optional[tuple[int, int]]:
    """
    Returns tile coordinates at mouse position on the fiven board.

    :param board: A game board to search the tile.
    :return: A tuple of tile coordinates in (x, y) format.
    """
    mouse_coords = pygame.mouse.get_pos()
    current_tile = get_tile_at_pixel(mouse_coords, board)
    return current_tile


def highlight_tile_under_mouse(game_data: GameDataType) -> GameDataType:
    """
    Highlights tile at the current position of the mouse cursor,
    if cursor is over enemy board.

    :param game_data: A TypedDict of game state variables.
    :return: A TypedDict of game state variables.
    """
    last_tile = game_data['mouse_position_tile']
    enemy_board = game_data['enemy_board']

    current_tile = get_mouse_position(enemy_board)
    enemy_board = update_highlighted_tile(current_tile, last_tile, enemy_board)

    game_data['mouse_position_tile'] = current_tile
    game_data['enemy_board'] = enemy_board
    return game_data


def handle_board_click(click_coords: tuple[int, int],
                       board: GameBoardType
                       ) -> Optional[tuple[int, int]]:
    """
    Returns board coordinates of the mouse clicked tile if it exists
    and was clicked for the first time, else None.

    :param click_coords: Mouse click pixel coordinates in (x, y)
    format.
    :param board: The board which a tile was clicked.
    :return: Board coordinates of the player move tile or None.
    """
    tile_coords = get_tile_at_pixel(click_coords, board)

    if tile_coords is not None:
        tile = get_reference_to_tile(tile_coords, board)

        if tile['hit_result'] is None:
            return tile_coords
    return None


def quit_program() -> None:
    """Finalizes the program execution."""
    pygame.quit()
    sys.exit()


def handle_button_click(click_coords: tuple[int, int],
                        buttons: dict[str, TextSurfaceType],
                        game_data: GameDataType) -> GameDataType:
    """
    Does appropriate action if one of the menu buttons have been
    pressed.

    :param click_coords: Mouse click pixel coordinates in (x, y)
    format.
    :param buttons: A dictionary containing menu buttons
    of TextSurfaceType.
    :param game_data: A TypedDict of game state variables.
    :return: An updated TypedDict of game state variables.
    """
    newgame_was_pressed = buttons['newgame']['rect'].collidepoint(click_coords)
    reveal_was_pressed = buttons['reveal_enemy']['rect'].collidepoint(
        click_coords)
    quit_was_pressed = buttons['quit']['rect'].collidepoint(click_coords)

    if newgame_was_pressed:
        game_data = set_up_new_game()

    elif reveal_was_pressed:
        enemy_is_hidden = game_data['enemy_is_hidden']
        if enemy_is_hidden:
            game_data['enemy_is_hidden'] = False
        else:
            game_data['enemy_is_hidden'] = True

    elif quit_was_pressed:
        quit_program()

    return game_data


def handle_events(game_data: GameDataType,
                  buttons: dict[str, TextSurfaceType]
                  ) -> tuple[GameDataType, Optional[tuple[int, int]]]:
    """
    Handles events of the game: mouse movement and click, closing
    the game window or pressing ESC button.

    :param game_data: A TypedDict of game state variables.
    :param buttons: A dictionary containing menu buttons
    of TextSurfaceType.
    :return: A tuple of updated game data and board
    coordinates of a player move in format (x, y).
    """
    player_move = None
    enemy_board = game_data['enemy_board']

    game_data = highlight_tile_under_mouse(game_data)

    for event in pygame.event.get():
        window_was_closed = (event.type == QUIT)
        esc_was_pressed = (event.type == KEYUP and event.key == K_ESCAPE)
        mouse_was_clicked = (event.type == MOUSEBUTTONUP)

        if window_was_closed or esc_was_pressed:
            quit_program()

        elif mouse_was_clicked:
            player_move = handle_board_click(event.pos, enemy_board)
            game_data = handle_button_click(event.pos, buttons, game_data)

    return game_data, player_move


def mark_shot_result(tile_coords: tuple[int, int],
                     board: GameBoardType) -> GameBoardType:
    """
    Writes shot result to the game board data structure.

    :param tile_coords: The tile that was shot.
    :param board: A game board of GameBoardType(TypedDict).
    :return: An updated game board of GameBoardType(TypedDict).
    """
    tile = get_reference_to_tile(tile_coords, board)

    if tile['is_empty']:
        tile['hit_result'] = 'miss'
    else:
        tile['hit_result'] = 'damage'
        board['targets'].remove(tile_coords)
    return board


def victory_achieved(board: GameBoardType) -> bool:
    """
    Checks if victory has been achieved on the given board.

    :param board: A game board of GameBoardType(TypedDict) to check.
    :return: True, if victory has been achieved, else False.
    """
    all_ships_destroyed = len(board['targets']) == 0

    if all_ships_destroyed:
        return True
    else:
        return False


def handle_player_move(player_move_coords: tuple[int, int],
                       game_data: GameDataType
                       ) -> GameDataType:
    """
    Updates the enemy board by marking the result of the given shot
    coordinates. If the player has won, ends the game.

    :param game_data: A TypedDict of game state variables.
    :param player_move_coords: A tuple of the given shot coordinates
    in (x, y) format.
    :return: A TypedDict of game state variables with updated enemy
    board.
    """
    board = game_data['enemy_board']

    game_data['enemy_board'] = mark_shot_result(
        tile_coords=player_move_coords,
        board=board)

    if victory_achieved(board):
        game_data['game_is_over'] = True
        game_data['screen_message'] = make_text_surface(
            text=ENDGAME_WIN_TEXT,
            topleft=MESSAGE_TOPLEFT)
    return game_data


def make_ai_move(game_data: GameDataType) -> GameDataType:
    """
    Updates the player board by marking the result of AI move.
    If the AI has won, ends the game.

    :param game_data: A TypedDict of game state variables.
    :return: A TypedDict of game state variables with updated player
    board and AI data.
    """
    board = game_data['player_board']
    ai_data = game_data['ai_data']
    last_move = game_data['last_ai_move']

    move, ai_data = get_ai_move(ai_data, board)
    board = mark_shot_result(move, board)
    board = update_highlighted_tile(move, last_move, board)

    game_data['last_ai_move'] = move

    if victory_achieved(board):
        game_data['screen_message'] = make_text_surface(
            text=ENDGAME_DEFEAT_TEXT,
            topleft=MESSAGE_TOPLEFT)
        game_data['game_is_over'] = True
    return game_data
