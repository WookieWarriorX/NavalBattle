# -*- coding: utf-8 -*-
import random
from typing import Optional

from constants import (
    AIDataType, GameBoardType, BOARD_HEIGHT_IN_TILES, BOARD_WIDTH_IN_TILES,
    ATTACK_DIRECTIONS_TEMPLATE, REVERSED_ATTACK_DIRECTIONS,
    SHIP_COUNTS, SHIP_SIZES)


def set_up_ai() -> AIDataType:
    """
    Creates a new AI data.

    :return: An AI data structure of AIDataType (TypedDict).
    """
    # Each tile is an available move at the beginning
    available_moves = [(board_x, board_y)
                       for board_x in range(BOARD_HEIGHT_IN_TILES)
                       for board_y in range(BOARD_WIDTH_IN_TILES)]

    # Create a list of ships placed on the game board
    ships_on_board = []
    for count, size in zip(SHIP_COUNTS, SHIP_SIZES):
        for _ in range(count):
            ships_on_board.append(size)

    ai_data: AIDataType
    ai_data = {'state': 'search',
               'attack_direction': None,
               'available_moves': available_moves,
               'hit_moves': [],
               'available_directions': list(ATTACK_DIRECTIONS_TEMPLATE),
               'ships_on_board_by_size': ships_on_board}
    return ai_data


def get_move_by_direction(ai_data: AIDataType
                          ) -> tuple[int, int]:
    """
    Calculates next shot coordinates based on last hit and attack
    direction.

    :param ai_data: A TypedDict of AI state variables.
    :return: Coordinates of the next shot in (x, y) format.
    """
    last_hit = ai_data['hit_moves'][-1]
    direction = ai_data['attack_direction']

    if direction == 'right':
        move_coords = last_hit[0] + 1, last_hit[1]
    elif direction == 'left':
        move_coords = last_hit[0] - 1, last_hit[1]
    elif direction == 'down':
        move_coords = last_hit[0], last_hit[1] + 1
    elif direction == 'up':
        move_coords = last_hit[0], last_hit[1] - 1
    else:
        raise RuntimeError("AI attack directions error. "
                           "Direction must be 'up', 'down', "
                           "'left' or 'right'!")
    return move_coords


def remove_destroyed_ship(ai_data):
    """
    Removes the destroyed ship from the list of ships on board.

    :param ai_data: A TypedDict of AI state variables.
    :return: An AI data with updated list of ships on board.
    """
    destroyed_ship_length = len(ai_data['hit_moves'])
    ai_data['ships_on_board_by_size'].remove(destroyed_ship_length)
    return ai_data


def remove_ship_spacing(ai_data):
    """
    Removes the destroyed ship spacing from the list of available moves.

    :param ai_data: A TypedDict of AI state variables.
    :return: An AI data with updated available moves list.
    """
    destroyed_ship = ai_data['hit_moves']

    for tile in destroyed_ship:
        for x_shift in range(-1, 2):
            for y_shift in range(-1, 2):
                adjacent_tile = (tile[0] + x_shift, tile[1] + y_shift)
                if adjacent_tile in ai_data['available_moves']:
                    ai_data['available_moves'].remove(adjacent_tile)
    return ai_data


def switch_ai_to_search(ai_data: AIDataType) -> AIDataType:
    """
    Switches the AI to the search state.

    :param ai_data: A TypedDict of AI state variables.
    :return: An AI data in search state.
    """
    ai_data['state'] = 'search'
    ai_data['hit_moves'].clear()
    ai_data['available_directions'] = list(ATTACK_DIRECTIONS_TEMPLATE)
    return ai_data


def finish_attack(ai_data: AIDataType) -> AIDataType:
    """
    Ends the current attack sequence by updating AI data with
    attack results and switching the AI to the search state.

    :param ai_data: A TypedDict of AI state variables.
    :return: An AI data in search state with deleted destroyed ship
    and its spacing.
    """
    ai_data = remove_destroyed_ship(ai_data)
    ai_data = remove_ship_spacing(ai_data)
    ai_data = switch_ai_to_search(ai_data)
    return ai_data


def choose_random_direction(available_directions: list[str]) -> str:
    """
    Returns random direction from the list of available.

    :param available_directions: The list of available directions.
    :return: An attack direction ('up', 'down', 'right' or 'left').
    """
    return random.choice(available_directions)


def choose_attack_direction(ai_data: AIDataType
                            ) -> tuple[str, AIDataType]:
    """
    Chooses next attack direction randomly from the list of currently
    available to the AI.

    :param ai_data: A TypedDict of AI state variables.
    :return: An attack direction ('up', 'down', 'right' or 'left') and
    AI data with updated available directions list.
    """
    direction = choose_random_direction(ai_data['available_directions'])
    ai_data['available_directions'].remove(direction)
    ai_data['attack_direction'] = direction
    return direction, ai_data


def attack_after_first_hit(ai_data: AIDataType
                           ) -> tuple[Optional[tuple[int, int]], AIDataType]:
    """
    Returns next attack move coordinates after the FIRST hit
    at the enemy ship based on the following logic.

    The goal is to find the direction where the rest of the ship is
    by achieving a second hit.
    1) Probe each of four directions randomly to find where the rest
    of the ship is.
    2) If all directions have been probed unsuccessfully, consider ship
    destroyed and finish the attack.

    :param ai_data: A TypedDict of AI state variables.
    :return: Next shot coordinates in (x,y) format and AI data with
    updated attack direction.
    """
    while True:
        all_directions_probed = len(ai_data['available_directions']) == 0

        if all_directions_probed:
            move_coords = None
            ai_data = finish_attack(ai_data)
            break
        else:
            direction, ai_data = choose_attack_direction(ai_data)
            move_coords = get_move_by_direction(ai_data)

            if move_coords in ai_data['available_moves']:
                break
    return move_coords, ai_data


def get_reversed_move(ai_data: AIDataType
                      ) -> tuple[tuple[int, int], AIDataType]:
    """
    Returns move coordinates in the opposite direction to the previous
    one, starting from the first hit at the enemy ship.

    :param ai_data: A TypedDict of AI state variables.
    :return: Coordinates of the reversed move in (x,y) format.
    """
    old_direction = ai_data['attack_direction']
    first_hit = ai_data['hit_moves'][0]

    direction_index = ATTACK_DIRECTIONS_TEMPLATE.index(old_direction)
    direction = REVERSED_ATTACK_DIRECTIONS[direction_index]
    ai_data['attack_direction'] = direction

    if direction == 'right':
        move_coords = first_hit[0] + 1, first_hit[1]
    elif direction == 'left':
        move_coords = first_hit[0] - 1, first_hit[1]
    elif direction == 'down':
        move_coords = first_hit[0], first_hit[1] + 1
    elif direction == 'up':
        move_coords = first_hit[0], first_hit[1] - 1
    else:
        raise RuntimeError("Reversed AI attack directions error. "
                           "Direction must be 'up', 'down', "
                           "'left' or 'right'!")
    return move_coords, ai_data


def attack_after_second_hit(ai_data: AIDataType
                            ) -> tuple[Optional[tuple[int, int]], AIDataType]:
    """
    Returns next attack move coordinates after the SECOND hit
    at enemy ship based on the following logic.

    The goal is to destroy parts of the damaged ship left after first
    two hits.
    1) Try to attack in the old direction.
    2) Try to attack in the reverse direction.
    3) If no move is possible, consider ship destroyed and finish
    the attack.

    :param ai_data: A TypedDict of AI state variables.
    :return: Next shot coordinates in (x,y) format and AI data with
    updated attack direction.
    """
    available_moves = ai_data['available_moves']
    move_coords: Optional[tuple[int, int]] = get_move_by_direction(ai_data)

    if move_coords not in available_moves:
        move_coords, ai_data = get_reversed_move(ai_data)

        if move_coords not in available_moves:
            move_coords = None
            ai_data = finish_attack(ai_data)

    return move_coords, ai_data


def attack_ship(ai_data: AIDataType
                ) -> tuple[Optional[tuple[int, int]], AIDataType]:
    """
    Executes an attacking action based on the following logic
    to choose the next attack move.

    Before each turn, check if an undestroyed ship larger than
    the hitted target exists on board.
    The attack is divided in two steps:
    1) Try to find the direction where the rest of the ship is, if any.
    2) After the second hit, destroy the rest of the ship, if any.
    If no attacking move available, the AI returns to the search state.

    :param ai_data: A TypedDict of AI state variables.
    :return: Next shot coordinates in (x,y) format and updated AI data.
    """
    current_biggest_ship = max(ai_data['ships_on_board_by_size'])
    hitted_ship_length = len(ai_data['hit_moves'])

    if hitted_ship_length < current_biggest_ship:
        first_time_hit = len(ai_data['hit_moves']) == 1

        if first_time_hit:
            move_coords, ai_data = attack_after_first_hit(ai_data)
        else:
            move_coords, ai_data = attack_after_second_hit(ai_data)
    else:
        move_coords = None
        ai_data = finish_attack(ai_data)
    return move_coords, ai_data


def make_random_move(available_moves: list[tuple[int, int]]
                     ) -> tuple[int, int]:
    """
    Returns random move from the list of available.

    :param available_moves: List of available moves coordinates
    in (x, y) format.
    :return: A tuple of move coordinates in (x, y) format.
    """
    return random.choice(available_moves)


def choose_next_move(ai_data: AIDataType
                     ) -> tuple[tuple[int, int], AIDataType]:
    """
    Launches move choosing scenario based on the current AI state.

    :param ai_data: A TypedDict of AI state variables.
    :return: Next shot coordinates in (x,y) format and updated AI data.
    """
    move_coords = None

    if ai_data['state'] == 'attack':
        move_coords, ai_data = attack_ship(ai_data)
    if ai_data['state'] == 'search':
        move_coords = make_random_move(ai_data['available_moves'])
    else:
        # If AI could not find a target during the attack
        # and did not switch to search
        if move_coords is None:
            raise RuntimeError("AI target choosing error. "
                               "The AI can not find an attacking move and "
                               "did not switched to search.")
    return move_coords, ai_data


def update_move_list(move_coords: tuple[int, int],
                     ai_data: AIDataType) -> AIDataType:
    """
    Deletes the given move from the list of available.

    :param move_coords: Coordinates of the move to check
    in (x,y) format.
    :param ai_data: A TypedDict of AI state variables.
    :return: An AI data with updated available move list.
    """
    ai_data['available_moves'].remove(move_coords)
    return ai_data


def ship_was_hitted(move_coords: tuple[int, int],
                    board: GameBoardType) -> bool:
    """
    Checks if the given move hits an enemy ship.

    :param move_coords: Coordinates of the move to check
    in (x,y) format.
    :param board: A game board to check hit.
    :return: True if move hits an enemy ship, else None.
    """
    board_x, board_y = move_coords
    if board['tiles'][board_x][board_y]['is_empty'] is False:
        return True
    else:
        return False


def handle_hit(move_coords: tuple[int, int],
               ai_data: AIDataType) -> AIDataType:
    """
    Handles hit at an enemy ship by adding hit coordinates to the AI
    memory and switching the AI to attack state if needed.

    :param move_coords: Coordinates of the hit move in (x,y) format.
    :param ai_data: A TypedDict of AI state variables.
    :return: An AI data with updated hit move list.
    """
    ai_data['hit_moves'].append(move_coords)

    if ai_data['state'] == 'search':
        ai_data['state'] = 'attack'
    return ai_data


def get_ai_move(ai_data: AIDataType,
                board: GameBoardType
                ) -> tuple[tuple[int, int], AIDataType]:
    """
    Returns next AI move coordinates.

    :param ai_data: A TypedDict of AI state variables.
    :param board: The game board where to search move.
    :return: Next shot coordinates in (x,y) format and updated AI data.
    """
    move_coords, ai_data = choose_next_move(ai_data)
    ai_data = update_move_list(move_coords, ai_data)

    if ship_was_hitted(move_coords, board):
        ai_data = handle_hit(move_coords, ai_data)
    return move_coords, ai_data
