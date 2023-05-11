# -*- coding: utf-8 -*-
import pygame
from pygame.font import Font

from constants import (
    TextSurfaceType, TileDataType, GameBoardType, GameDataType,
    DISPLAY_SURFACE, BASIC_FONT, TEXT_COLOR, BG_COLOR, WHITE, BLACK,
    GRAY, LIGHT_GRAY, DARK_COLORS, LIGHT_COLORS,
    TILE_SIZE, GRID_STEP, GRID_WIDTH, MISS_SIGN_RADIUS,
    BOARD_WIDTH_IN_PIXELS, BOARD_HEIGHT_IN_PIXELS,
    BOARD_WIDTH_IN_TILES, BOARD_HEIGHT_IN_TILES,
    NEWGAME_BUTTON_TEXT, NEWGAME_BUTTON_TOPLEFT, BUTTON_COLOR,
    REVEAL_BUTTON_TEXT, REVEAL_BUTTON_TOPLEFT,
    QUIT_BUTTON_TEXT, QUIT_BUTTON_TOPLEFT,
    PLAYER_BOARD_TITLE_TEXT, PLAYER_BOARD_TITLE_TOPLEFT,
    AI_BOARD_TITLE_TEXT, AI_BOARD_TITLE_TOPLEFT)


def make_text_surface(text: str,
                      topleft: tuple[int, int],
                      font: Font = BASIC_FONT,
                      text_color: tuple[int, int, int] = TEXT_COLOR,
                      bgcolor: tuple[int, int, int] = BG_COLOR
                      ) -> TextSurfaceType:
    """
    Creates a surface with text inside.

    :param text: A text to draw on the surface.
    :param font: The Font object from "pygame.font" module
    of Pygame package.
    :param text_color: A text color in (R, G, B) format.
    :param bgcolor: A background color of the surface
    in (R, G, B) format.
    :param topleft: The top left corner coordinates
    of the surface in (x, y) format.
    :return: A TypeDict of surface and rectangular objects
    from Pygame in {'surf': Surface, 'rect': Rect} format.
    """
    text_surf = font.render(text, True, text_color, bgcolor)
    border_rect = text_surf.get_rect()
    border_rect.topleft = topleft

    text_surface: TextSurfaceType = {'surf': text_surf, 'rect': border_rect}
    return text_surface


def make_menu_buttons() -> dict[str, TextSurfaceType]:
    """
    Creates a dictionary containing 'New game', 'Show enemy',
    and 'Quit' buttons.

    :return: A dictionary containing buttons of TextSurfaceType.
    """
    newgame_button = make_text_surface(text=NEWGAME_BUTTON_TEXT,
                                       topleft=NEWGAME_BUTTON_TOPLEFT,
                                       bgcolor=BUTTON_COLOR)
    reveal_enemy_button = make_text_surface(text=REVEAL_BUTTON_TEXT,
                                            topleft=REVEAL_BUTTON_TOPLEFT,
                                            bgcolor=BUTTON_COLOR)
    quit_button = make_text_surface(text=QUIT_BUTTON_TEXT,
                                    topleft=QUIT_BUTTON_TOPLEFT,
                                    bgcolor=BUTTON_COLOR)
    buttons = {'newgame': newgame_button,
               'reveal_enemy': reveal_enemy_button,
               'quit': quit_button}
    return buttons


def make_board_titles() -> dict[str, TextSurfaceType]:
    """
    Creates a dictionary containing player and enemy boards titles.

    :return: A dictionary containing board titles of TextSurfaceType.
    """
    player_board_title = make_text_surface(text=PLAYER_BOARD_TITLE_TEXT,
                                           topleft=PLAYER_BOARD_TITLE_TOPLEFT)
    ai_board_title = make_text_surface(text=AI_BOARD_TITLE_TEXT,
                                       topleft=AI_BOARD_TITLE_TOPLEFT)
    titles = {'player_board': player_board_title,
              'ai_board': ai_board_title}
    return titles


def get_tile_color(tile: TileDataType,
                   is_hidden: bool) -> tuple[int, int, int]:
    """
    Returns a color of the given tile.

    :param tile: A tile to choose a color of TileDataType.
    :param is_hidden: 'True' if the tile belongs to the enemy
    and needs to be hidden.
    :return: The tile color in (R, G, B) format.
    """
    if is_hidden:
        tile_was_hitted = tile['hit_result']
        if tile_was_hitted:
            color = BG_COLOR
        else:
            # Unhitted (closed) enemy tile - gray plug
            color = GRAY
    else:
        color = tile['color']
    return color


def draw_miss_sign(tile: TileDataType,
                   hit_color: tuple[int, int, int]) -> None:
    """
    Draws miss sign (dot) inside the given tile.

    :param tile: A tile of TileDataType to draw the sign.
    :param hit_color: The sign color in (R, G, B) format.
    :return: None.
    """
    center_point = (tile['pixel_x'] + TILE_SIZE / 2,
                    tile['pixel_y'] + TILE_SIZE / 2)
    pygame.draw.circle(surface=DISPLAY_SURFACE,
                       color=hit_color,
                       center=center_point,
                       radius=MISS_SIGN_RADIUS)


def draw_hit_sign(tile: TileDataType,
                  hit_color: tuple[int, int, int]) -> None:
    """
    Draws the hit sign (cross) inside the given tile.

    :param tile: A tile of TileDataType to draw the sign.
    :param hit_color: The sign color in (R, G, B) format.
    :return: None.
    """
    upper_left = (tile['pixel_x'], tile['pixel_y'])
    lower_right = (tile['pixel_x'] + TILE_SIZE, tile['pixel_y'] + TILE_SIZE)
    pygame.draw.line(surface=DISPLAY_SURFACE,
                     color=hit_color,
                     start_pos=upper_left,
                     end_pos=lower_right,
                     width=GRID_WIDTH)

    upper_right = (tile['pixel_x'] + TILE_SIZE, tile['pixel_y'])
    lower_left = (tile['pixel_x'], tile['pixel_y'] + TILE_SIZE)
    pygame.draw.line(surface=DISPLAY_SURFACE,
                     color=hit_color,
                     start_pos=upper_right,
                     end_pos=lower_left,
                     width=GRID_WIDTH)


def draw_hit_result(tile: TileDataType,
                    is_hidden: bool) -> None:
    """
    Draws hit result in a tile: damage (cross) or miss (dot).

    :param tile: A tile of TileDataType to draw hit result.
    :param is_hidden: 'True' if the tile belongs to the enemy
    and needs to be hidden.
    :return: None.
    """
    hit_color = WHITE

    if tile['hit_result'] == 'miss':
        draw_miss_sign(tile, hit_color)

    elif tile['hit_result'] == 'damage':
        if not is_hidden:
            hit_color = BLACK
        draw_hit_sign(tile, hit_color)


def get_lighter_shade(color: tuple[int, int, int]) -> tuple[int, int, int]:
    """
    Returns lighter version of the given color.

    :param color: The dark shade in (R, G, B) format.
    :return: The light shade in (R, G, B) format.
    """
    color_index = DARK_COLORS.index(color)
    color = LIGHT_COLORS[color_index]
    return color


def draw_tile_background(tile: TileDataType,
                         color: tuple[int, int, int]) -> None:
    """
    Draws tile background filled with the given color.

    :param tile: A tile of TileDataType to draw background.
    :param color: The tile background color in (R, G, B) format.
    :return: None.
    """
    tile_rect = (tile['pixel_x'], tile['pixel_y'], TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(surface=DISPLAY_SURFACE,
                     color=color,
                     rect=tile_rect)


def draw_tile(tile: TileDataType,
              is_hidden: bool = False,
              need_highlight: bool = False) -> None:
    """
    Draws a tile of the given game board on the display surface.

    :param tile: A tile to draw.
    :param is_hidden: True if the board belongs to enemy and
    needs to be hidden.
    :param need_highlight: True, if the tile needs to be lighted.
    :return: None.
    """
    color = get_tile_color(tile, is_hidden)

    if tile['is_lighted'] or need_highlight:
        color = get_lighter_shade(color)

    draw_tile_background(tile, color)

    if tile['hit_result'] is not None:
        draw_hit_result(tile, is_hidden)


def draw_border(board: GameBoardType) -> None:
    """
    Draws border lines of the given board on the display surface.

    :param board: A board of GameBoardType(TypedDict) to draw borders.
    :return: None.
    """
    topleft_x = board['topleft']['pixel_x']
    topleft_y = board['topleft']['pixel_y']
    length_x = BOARD_WIDTH_IN_PIXELS + GRID_WIDTH
    length_y = BOARD_HEIGHT_IN_PIXELS + GRID_WIDTH

    border_rect = (topleft_x, topleft_y, length_x, length_y)
    pygame.draw.rect(surface=DISPLAY_SURFACE,
                     color=LIGHT_GRAY,
                     rect=border_rect,
                     width=GRID_WIDTH)


def draw_grid(board: GameBoardType) -> None:
    """
    Draws grid lines of the given board on the display surface.

    :param board: A board of GameBoardType(TypedDict) to draw grid.
    :return: None.
    """
    topleft_x = board['topleft']['pixel_x']
    topleft_y = board['topleft']['pixel_y']
    topright_x = topleft_x + BOARD_WIDTH_IN_PIXELS
    downleft_y = topleft_y + BOARD_HEIGHT_IN_PIXELS

    # Draw vertical grid lines
    for board_x in range(BOARD_WIDTH_IN_TILES):
        x = topleft_x + GRID_STEP * board_x
        pygame.draw.line(surface=DISPLAY_SURFACE,
                         color=LIGHT_GRAY,
                         start_pos=(x, topleft_y),
                         end_pos=(x, downleft_y),
                         width=GRID_WIDTH)
    # Draw horizontal grid lines
    for board_y in range(BOARD_HEIGHT_IN_TILES):
        y = topleft_y + GRID_STEP * board_y
        pygame.draw.line(surface=DISPLAY_SURFACE,
                         color=LIGHT_GRAY,
                         start_pos=(topleft_x, y),
                         end_pos=(topright_x, y),
                         width=GRID_WIDTH)


def draw_board(board: GameBoardType,
               is_hidden: bool = False) -> None:
    """
    Draws the given game board on the display surface.

    :param board: A game board of GameBoardType(TypedDict).
    :param is_hidden: 'True' if the board belongs to the enemy
    and needs to be hidden.
    :return: None.
    """
    draw_border(board)
    draw_grid(board)

    for board_x in range(BOARD_WIDTH_IN_TILES):
        for board_y in range(BOARD_HEIGHT_IN_TILES):
            tile = board['tiles'][board_x][board_y]
            draw_tile(tile, is_hidden)


def draw_game_screen(game_data: GameDataType,
                     titles: dict[str, TextSurfaceType],
                     buttons: dict[str, TextSurfaceType]) -> None:
    """
    Draws the game on the display surface.

    :param game_data: A TypedDict of game state variables.
    :param titles: A dictionary containing player and enemy boards
    titles of TextSurfaceType.
    :param buttons: A dictionary containing menu buttons
    of TextSurfaceType.
    :return: None.
    """
    screen_message = game_data['screen_message']
    player_board = game_data['player_board']
    enemy_board = game_data['enemy_board']
    enemy_is_hidden = game_data['enemy_is_hidden']

    DISPLAY_SURFACE.fill(BG_COLOR)
    DISPLAY_SURFACE.blit(screen_message['surf'], screen_message['rect'])

    for _, title in titles.items():
        DISPLAY_SURFACE.blit(title['surf'], title['rect'])
    draw_board(player_board)
    draw_board(enemy_board, is_hidden=enemy_is_hidden)

    for _, button in buttons.items():
        DISPLAY_SURFACE.blit(button['surf'], button['rect'])

    pygame.display.update()
