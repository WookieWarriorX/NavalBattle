# -*- coding: utf-8 -*-
import random

from constants import (
    GameBoardType, TileMatrixType, TargetListType, BOARD_WIDTH_IN_TILES,
    BOARD_HEIGHT_IN_TILES, GRID_STEP, GRID_WIDTH, DARK_TURQUOISE, SHIP_SIZES,
    SHIP_COUNTS, SHIP_COLORS)


def get_tile_pixel_coords(x: int, y: int,
                          board_topleft: tuple[int, int],
                          grid_step: int = GRID_STEP,
                          grid_width: int = GRID_WIDTH
                          ) -> tuple[int, int]:
    """
    Returns pixel tile coordinates by given board tile coordinates.

    :param x: The x coordinate of the tile.
    :param y: The y coordinate of the tile.
    :param board_topleft: Top left pixel coordinates of the board where tile
    is situated.
    :param grid_step: Interval between grid lines.
    :param grid_width: The width of the grid line.
    :return: Pixel coordinates of the given tile in (x, y) format.
    """
    board_topleft_x = board_topleft[0]
    board_topleft_y = board_topleft[1]

    pixel_x = board_topleft_x + x * grid_step + grid_width
    pixel_y = board_topleft_y + y * grid_step + grid_width
    return pixel_x, pixel_y


def get_new_board(topleft: tuple[int, int],
                  board_width: int = BOARD_WIDTH_IN_TILES,
                  board_height: int = BOARD_HEIGHT_IN_TILES,
                  empty_tile_color: tuple[int, int, int] = DARK_TURQUOISE
                  ) -> GameBoardType:
    """
    Creates an empty game board at given coordinates.

    :param topleft: The top left corner coordinates of the new board
    in (x, y) format.
    :param board_width: Board width in tiles.
    :param board_height: Board height in tiles.
    :param empty_tile_color: A color of empty tiles.
    :return: A new game board data structure of
    GameBoardType(TypedDict).
    """
    board_topleft_x = topleft[0]
    board_topleft_y = topleft[1]
    tile_matrix: TileMatrixType = []

    for board_x in range(board_width):
        tile_matrix.append([])
        for board_y in range(board_height):
            pixel_x, pixel_y = get_tile_pixel_coords(board_x, board_y,
                                                     topleft)

            tile_matrix[board_x].append({'pixel_x': pixel_x,
                                         'pixel_y': pixel_y,
                                         'board_x': board_x,
                                         'board_y': board_y,
                                         'is_empty': True,
                                         'is_for_spacing': False,
                                         'is_lighted': False,
                                         'hit_result': None,
                                         'color': empty_tile_color})
    board_targets: TargetListType = []
    new_board: GameBoardType
    new_board = {'tiles': tile_matrix,
                 'topleft': {'pixel_x': board_topleft_x,
                             'pixel_y': board_topleft_y},
                 'targets': board_targets}
    return new_board


def tile_is_on_board(board_x: int,
                     board_y: int,
                     board_width: int = BOARD_WIDTH_IN_TILES,
                     board_height: int = BOARD_HEIGHT_IN_TILES) -> bool:
    """
    Check if the tile is not off the board.

    :param board_x: The x-coordinate of the tile.
    :param board_y: The y-coordinate of the tile.
    :param board_width: The width of the game board in tiles.
    :param board_height: The height of the game board in tiles.
    :return: True if the tile is not off the board, else False.
    """
    x_is_within_board = (0 <= board_x < board_width)
    y_is_within_board = (0 <= board_y < board_height)
    if x_is_within_board and y_is_within_board:
        return True
    else:
        return False


def tile_is_ready_for_placement(board_x: int,
                                board_y: int,
                                board: GameBoardType) -> bool:
    """
    Checks if the tile is ready for ship placement.

    :param board_x: The x-coordinate of the tile.
    :param board_y: The y-coordinate of the tile.
    :param board: A game board to check the tile
    of GameBoardType(TypedDict).
    :return: True if tile is ready for ship placement, else False.
    """
    if tile_is_on_board(board_x, board_y):
        tile = board['tiles'][board_x][board_y]
        if tile['is_empty'] and not tile['is_for_spacing']:
            return True
    return False


def search_placement_ready_tiles(board: GameBoardType
                                 ) -> list[tuple[int, int]]:
    """
    Searches unused tiles on the board available for ship placement.

    :param board: A board to search tiles of GameBoardType(TypedDict).
    :return: A list of (x, y) tuples with coordinates
    of placement-ready tiles.
    """
    tiles = [(board_x, board_y)
             for board_x in range(BOARD_WIDTH_IN_TILES)
             for board_y in range(BOARD_HEIGHT_IN_TILES)
             if tile_is_ready_for_placement(board_x, board_y, board)]
    return tiles


def choose_orientation_randomly() -> str:
    """
    Randomly chooses horizontal or vertical orientation of the ship.
    :return: Ship orientation in 'horizontal' or 'vertical' format.
    """
    return random.choice(('horizontal', 'vertical'))


def select_random_tile(tiles: list[tuple[int, int]]) -> dict[str, int]:
    """
    Selects a random tile from the given list.

    :param tiles: A list of (x, y) tuples with
    tile coordinates to select.
    :return: A dictionary of selected tile coordinates
    in {'x': int, 'y': int} format.
    """
    tile = {}
    (tile['x'], tile['y']) = random.choice(tiles)
    return tile


def get_ship_body_coords(first_tile: dict[str, int],
                         length: int,
                         orientation: str) -> list[tuple[int, int]]:
    """
    Returns a list of tile coordinates of the ship body.

    :param first_tile: First (head) tile coordinates to start from
    in {'x': int, 'y': int} format.
    :param length: The length of the ship.
    :param orientation: The orientation of the placing ship can be
    'horizontal' or 'vertical'.
    :return: A list of (x, y) tuples with coordinates
    of placement-ready tiles.
    """
    ship_tiles = []
    for shift in range(length):
        if orientation == 'horizontal':
            board_x = first_tile['x'] + shift
            board_y = first_tile['y']
        elif orientation == 'vertical':
            board_x = first_tile['x']
            board_y = first_tile['y'] + shift
        else:
            raise ValueError("Ship tiles getting error. Invalid ship "
                             "orientation, must be 'horizontal' "
                             "or 'vertical'.")
        ship_tiles.append((board_x, board_y))
    return ship_tiles


def check_ship_placement_possibility(first_tile: dict[str, int],
                                     length: int,
                                     orientation: str,
                                     board: GameBoardType) -> bool:
    """
    Checks if a ship of the given length can be placed on the board,
    starting from the given tile.

    :param first_tile: First (head) tile coordinates to start from
    in {'x': int, 'y': int} format.
    :param length: The length of the ship to place.
    :param orientation: The orientation of the placing ship can be
    'horizontal' or 'vertical'.
    :param board: A game board of GameBoardType(TypedDict)
    to place the ship.
    :return: True if the ship can be placed, else False.
    """
    ship_tiles = get_ship_body_coords(first_tile, length, orientation)

    for board_x, board_y in ship_tiles:
        if not tile_is_ready_for_placement(board_x, board_y, board):
            return False
    return True


def place_ship_on_board(first_tile: dict[str, int],
                        length: int,
                        color: tuple[int, int, int],
                        orientation: str,
                        board: GameBoardType) -> GameBoardType:
    """
    Fills board tiles that belongs to the ship with the given color.

    :param first_tile: First (head) tile coordinates to start from
    in format {'x': int, 'y': int}.
    :param length: The length of the ship to place.
    :param color: A color to fill the ship tiles
    in (R, G, B) format.
    :param orientation: The orientation of the placing ship can be
    'horizontal' or 'vertical'.
    :param board: A game board of GameBoardType(TypedDict)
    to place the ship.
    :return: The game board with placed ship.
    """
    ship_tiles = get_ship_body_coords(first_tile, length, orientation)

    for board_x, board_y in ship_tiles:
        current_tile = board['tiles'][board_x][board_y]
        current_tile['color'] = color
        current_tile['is_empty'] = False
    return board


def mark_ship_spacing(first_tile: dict[str, int],
                      length: int,
                      orientation: str,
                      board: GameBoardType) -> GameBoardType:
    """
    Marks ship surrounding tiles as spacing.

    :param first_tile: First (head) tile coordinates to start from
    in format {'x': int, 'y': int}.
    :param length: The length of the ship.
    :param orientation: The orientation of the placing ship can be
    'horizontal' or 'vertical'.
    :param board: A game board of GameBoardType(TypedDict)
    to place the ship.
    :return: The game board with marked ship spacing.
    """
    for length_shift in range(-1, length + 1):
        for width_shift in (- 1, 0, 1):
            if orientation == 'horizontal':
                board_x = first_tile['x'] + length_shift
                board_y = first_tile['y'] + width_shift
            elif orientation == 'vertical':
                board_x = first_tile['x'] + width_shift
                board_y = first_tile['y'] + length_shift
            else:
                raise ValueError("Ship spacing marking error. Invalid ship "
                                 "orientation, must be 'horizontal' "
                                 "or 'vertical'.")

            if tile_is_ready_for_placement(board_x, board_y, board):
                current_tile = board['tiles'][board_x][board_y]
                current_tile['is_for_spacing'] = True
    return board


def place_ship_randomly(length: int,
                        color: tuple[int, int, int],
                        board: GameBoardType) -> GameBoardType:
    """
    Places a ship of the given length and color on random tiles
    of the game board.

    :param length: The length of the ship to place on board.
    :param color: A color of the ship in (R, G, B) format.
    :param board: A board of GameBoardType(TypedDict)
    to place the ship.
    :return: The game board with placed ship and marked ship spacing.
    """
    orientation = choose_orientation_randomly()
    available_tiles = search_placement_ready_tiles(board)

    while True:
        if len(available_tiles) > 0:
            selected_tile = select_random_tile(available_tiles)
        else:
            raise RuntimeError("Can't fit all ships on board! "
                               "Make ships smaller or decrease their numbers.")
        ship_can_be_placed = check_ship_placement_possibility(
            first_tile=selected_tile,
            length=length,
            orientation=orientation,
            board=board)

        if ship_can_be_placed:
            board = place_ship_on_board(first_tile=selected_tile,
                                        length=length,
                                        color=color,
                                        orientation=orientation,
                                        board=board)
            board = mark_ship_spacing(first_tile=selected_tile,
                                      length=length,
                                      orientation=orientation,
                                      board=board)
            return board
        # If the tile fails the check, remove it and repeat
        available_tiles.remove((selected_tile['x'], selected_tile['y']))


def place_ships_randomly(board: GameBoardType) -> GameBoardType:
    """
    Places full set of ships on game board randomly.

    :param board: A board of GameBoardType(TypedDict)
    to place ships.
    :return: The game board with placed ships.
    """
    total_ship_types_count = len(SHIP_SIZES)
    for i in range(total_ship_types_count):
        for _ in range(SHIP_COUNTS[i]):
            board = place_ship_randomly(length=SHIP_SIZES[i],
                                        color=SHIP_COLORS[i],
                                        board=board)
    return board


def fill_targets_list(board: GameBoardType) -> GameBoardType:
    """
    Fills the list of targets (ship tiles) present on the given board.

    :param board: A board of GameBoardType(TypedDict)
    to fill the list.
    :return: The game board with filled list of targets.
    """
    board['targets'] = [
        (board_x, board_y)
        for board_x in range(BOARD_WIDTH_IN_TILES)
        for board_y in range(BOARD_HEIGHT_IN_TILES)
        if not board['tiles'][board_x][board_y]['is_empty']]
    return board


def get_random_board(board_topleft: tuple[int, int]) -> GameBoardType:
    """
    Creates a new game board with randomly placed ships.

    :param board_topleft: The top left corner coordinates
    of the new board in format (x, y).
    :return: A game-ready board data structure
    of GameBoardType (TypedDict).
    """
    board = get_new_board(board_topleft)
    board = place_ships_randomly(board)
    board = fill_targets_list(board)
    return board
