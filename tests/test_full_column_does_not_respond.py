"""Component tests for Connect Four presses that should be rejected."""

import tests._utils


def test___column_is_full___same_column_pressed___extra_move_is_rejected(game_and_board):
    game, board = game_and_board

    for _ in range(6):
        assert board.press(0, 0)

    colors_before_extra_press = dict(board.colors)

    accepted = board.press(0, 0)

    assert not accepted
    assert board.key_states[(0, 0)]["enable"] is False
    assert board.colors == colors_before_extra_press


def player_token_for_state(connect_four_module, current_player_state):
    if current_player_state == connect_four_module.CellState.PLAYER_1:
        return "1"
    return "2"


def test___column_is_full___same_column_pressed___turn_indicator_stays_on_current_player(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board

    for _ in range(6):
        board.press(0, 0)

    expected_player = player_token_for_state(connect_four_module, game.current_player)
    expected_color = game.get_player_color(
        tests._utils.player_state(connect_four_module, expected_player)
    )
    indicator_color_before_extra_press = board.color_at(1, 0)

    board.press(0, 0)

    assert indicator_color_before_extra_press == expected_color
    assert board.color_at(1, 0) == expected_color
