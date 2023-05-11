import pytest

from board_generator import (get_new_board, place_ship_randomly,
                             get_random_board)


def test_get_new_board(player_board_params, new_player_board):
    # GIVEN board parameters, new board sample
    board_params = player_board_params
    sample_board = new_player_board

    # WHEN new board is generated
    new_board = get_new_board(topleft=board_params['topleft'],
                              board_width=board_params['width_in_tiles'],
                              board_height=board_params['height_in_tiles'],
                              empty_tile_color=board_params['empty_tile_color'])
    # THEN result matches the sample
    assert new_board == sample_board


def test_place_ship_randomly(new_player_board, player_board_sample,
                             patch_random_for_player):
    # GIVEN empty board, fullfilled board sample
    empty_board = new_player_board
    sample_board = player_board_sample
    # AND ship parameters
    length = 4
    color = (155,   0,   0)
    ship_tiles = ((5, 0), (6, 0), (7, 0), (8, 0))

    # WHEN placing ship on board
    resulting_board = place_ship_randomly(length, color, empty_board)
    # THEN every ship tile matches with the sample
    for x, y in ship_tiles:
        resulting_tile = resulting_board['tiles'][x][y]
        sample_tile = sample_board['tiles'][x][y]
        assert resulting_tile == sample_tile


@pytest.mark.parametrize(
    'board_params, sample_board, patch_random',
    [('player_board_params', 'player_board_sample', 'patch_random_for_player'),
     ('enemy_board_params', 'enemy_board_sample', 'patch_random_for_enemy')],
    ids=['player_board', 'enemy_board'])
def test_get_random_board(board_params, sample_board, patch_random, request):
    # PATCH random choice
    request.getfixturevalue(patch_random)
    # GIVEN new board topleft and game-ready board sample
    board_params = request.getfixturevalue(board_params)
    board_topleft = board_params['topleft']
    sample_board = request.getfixturevalue(sample_board)

    # WHEN generating new board
    board = get_random_board(board_topleft)
    # THEN generated board matches the sample
    assert board == sample_board
