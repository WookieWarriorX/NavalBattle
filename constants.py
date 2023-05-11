# -*- coding: utf-8 -*-
from typing import TypedDict, Optional

import pygame
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface


#                    R    G    B
BLACK           = (  0,   0,   0)
WHITE           = (255, 255, 255)
DARK_GRAY       = ( 90,  90,  90)
GRAY            = (180, 180, 180)
LIGHT_GRAY      = (220, 220, 220)
RED             = (155,   0,   0)
LIGHT_RED       = (255,   0,   0)
GREEN           = (  0, 155,   0)
LIGHT_GREEN     = (  0, 255,   0)
BLUE            = (  0,   0, 155)
LIGHT_BLUE      = (  0,   0, 255)
YELLOW          = (155, 155,   0)
LIGHT_YELLOW    = (255, 255,   0)
DARK_TURQUOISE  = (  3,  54,  73)
TURQUOISE       = (  3, 123, 143)

DARK_COLORS = (BLACK, GRAY, RED, GREEN, BLUE, YELLOW, DARK_TURQUOISE)
LIGHT_COLORS = (DARK_GRAY, LIGHT_GRAY, LIGHT_RED, LIGHT_GREEN,
                LIGHT_BLUE, LIGHT_YELLOW, TURQUOISE)
BG_COLOR = DARK_TURQUOISE
BUTTON_COLOR = TURQUOISE
TEXT_COLOR = WHITE

FPS = 60
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 720
WINDOW_CAPTION = "Naval Battle"

BOARD_WIDTH_IN_TILES = 10
BOARD_HEIGHT_IN_TILES = 10
TILE_SIZE = 38
GRID_WIDTH = 2

GRID_STEP = TILE_SIZE + GRID_WIDTH
BOARD_WIDTH_IN_PIXELS = GRID_STEP * BOARD_WIDTH_IN_TILES
BOARD_HEIGHT_IN_PIXELS = GRID_STEP * BOARD_HEIGHT_IN_TILES
DISTANCE_BEETWEEN_BOARDS = 40
X_MARGIN = (WINDOW_WIDTH - (2 * BOARD_WIDTH_IN_PIXELS
                            + DISTANCE_BEETWEEN_BOARDS)) // 2
Y_MARGIN = (WINDOW_HEIGHT - BOARD_HEIGHT_IN_PIXELS) // 2
PLAYER_BOARD_TOPLEFT = (X_MARGIN, Y_MARGIN)
ENEMY_BOARD_TOPLEFT = (X_MARGIN + BOARD_WIDTH_IN_PIXELS
                       + DISTANCE_BEETWEEN_BOARDS, Y_MARGIN)

CARRIER_SIZE = 4  # default air carrier is 4-tile ship
CARRIER_COUNT = 1
CARRIER_COLOUR = RED
CRUISER_SIZE = 3  # default cruiser is 3-tile ship
CRUISER_COUNT = 2
CRUISER_COLOUR = GREEN
DESTROYER_SIZE = 2  # default destroyer is 2-tile ship
DESTROYER_COUNT = 3
DESTROYER_COLOUR = BLUE
FRIGATE_SIZE = 1  # default frigate is 1-tile ship
FRIGATE_COUNT = 4
FRIGATE_COLOUR = YELLOW
SHIP_SIZES = (CARRIER_SIZE, CRUISER_SIZE, DESTROYER_SIZE, FRIGATE_SIZE)
SHIP_COUNTS = (CARRIER_COUNT, CRUISER_COUNT, DESTROYER_COUNT, FRIGATE_COUNT)
SHIP_COLORS = (CARRIER_COLOUR, CRUISER_COLOUR,
               DESTROYER_COLOUR, FRIGATE_COLOUR)

BASIC_FONT_NAME = 'freesansbold.ttf'
BASIC_FONT_SIZE = 20

MESSAGE_TOPLEFT = (10, 30)
STARTGAME_TEXT = ("Welcome aboard, admiral! "
                  "Choose your targets on the right board.")
ENDGAME_WIN_TEXT = "Congratulations, admiral! You have won the battle!!!"
ENDGAME_DEFEAT_TEXT = "Sadly, you have loose the battle..."

NEWGAME_BUTTON_TEXT = "New Game"
NEWGAME_BUTTON_TOPLEFT = (WINDOW_WIDTH - 160, WINDOW_HEIGHT - 90)
REVEAL_BUTTON_TEXT = "Reveal AI board"
REVEAL_BUTTON_TOPLEFT = (WINDOW_WIDTH - 160, WINDOW_HEIGHT - 60)
QUIT_BUTTON_TEXT = "Quit"
QUIT_BUTTON_TOPLEFT = (WINDOW_WIDTH - 160, WINDOW_HEIGHT - 30)
PLAYER_BOARD_TITLE_TEXT = "Player board"
PLAYER_BOARD_TITLE_TOPLEFT = (X_MARGIN + 140, Y_MARGIN - 30)
AI_BOARD_TITLE_TEXT = "AI board"
AI_BOARD_TITLE_TOPLEFT = (
    X_MARGIN + 160 + BOARD_WIDTH_IN_PIXELS + DISTANCE_BEETWEEN_BOARDS,
    Y_MARGIN - 30)

ATTACK_DIRECTIONS_TEMPLATE = ('up', 'down', 'left', 'right')
REVERSED_ATTACK_DIRECTIONS = ('down', 'up', 'right', 'left')
MISS_SIGN_RADIUS = 4

TextSurfaceType = TypedDict('TextSurfaceType', {'surf': Surface,
                                                'rect': Rect})
TileDataType = TypedDict('TileDataType', {'pixel_x': int,
                                          'pixel_y': int,
                                          'board_x': int,
                                          'board_y': int,
                                          'is_empty': bool,
                                          'is_for_spacing': bool,
                                          'is_lighted': bool,
                                          'hit_result': Optional[str],
                                          'color': tuple[int, int, int]})
TileMatrixType = list[list[TileDataType]]
TargetListType = list[tuple[int, int]]
GameBoardType = TypedDict('GameBoardType', {'tiles': TileMatrixType,
                                            'topleft': dict[str, int],
                                            'targets': TargetListType})
AIDataType = TypedDict('AIDataType',
                       {'state': str,
                        'attack_direction': Optional[str],
                        'available_moves': list[tuple[int, int]],
                        'hit_moves': list[tuple[int, int]],
                        'available_directions': list[str],
                        'ships_on_board_by_size': list[int]})
GameDataType = TypedDict('GameDataType',
                         {'game_is_over': bool,
                          'enemy_is_hidden': bool,
                          'screen_message': TextSurfaceType,
                          'player_board': GameBoardType,
                          'enemy_board': GameBoardType,
                          'ai_data': AIDataType,
                          'last_ai_move': Optional[tuple[int, int]],
                          'mouse_position_tile': Optional[tuple[int, int]]})

DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.font.init()  # needed to initialize font
BASIC_FONT = pygame.font.Font(BASIC_FONT_NAME, BASIC_FONT_SIZE)
