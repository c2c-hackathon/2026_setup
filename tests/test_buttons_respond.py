"""Component tests for Connect Four button presses that should be accepted."""


def test___new_game___column_pressed___piece_drops_to_bottom_row(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board

    board.press(0, 0)

    assert board.color_at(0, 7) == game.get_player_color(connect_four_module.CellState.PLAYER_1)
    assert board.color_at(0, 6) == game.get_player_color(connect_four_module.CellState.EMPTY)


def test___new_game___column_pressed_twice___pieces_stack_and_turn_indicator_alternates(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board

    board.press(3, 0)

    assert board.color_at(3, 7) == game.get_player_color(connect_four_module.CellState.PLAYER_1)
    assert board.color_at(0, 0) == game.get_player_color(connect_four_module.CellState.PLAYER_2)

    board.press(3, 0)

    assert board.color_at(3, 6) == game.get_player_color(connect_four_module.CellState.PLAYER_2)
    assert board.color_at(0, 0) == game.get_player_color(connect_four_module.CellState.PLAYER_1)
