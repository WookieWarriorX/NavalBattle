import copy

import pytest

from ai import set_up_ai, attack_after_first_hit


def test_set_up_ai(new_ai_data):
    # GIVEN new ai data sample
    sample = new_ai_data

    # WHEN creating a new ai data
    ai_data = set_up_ai()
    # THEN result matches with the sample
    assert ai_data == sample


def test_attack_after_first_hit(first_step_ai_data, patch_random_for_ai):
    # GIVEN the starting AI data and coords of the correct move
    starting_ai = first_step_ai_data
    correct_move = (9, 7)
    # AND resulting state of AI
    resulting_ai = copy.deepcopy(starting_ai)
    resulting_ai['attack_direction'] = 'up'
    resulting_ai['available_directions'].remove('up')

    # WHEN executing attack after first hit
    move_coords, ai_data = attack_after_first_hit(starting_ai)
    # THEN move coordinates matches with correct answer
    assert move_coords == correct_move
    assert ai_data == resulting_ai
