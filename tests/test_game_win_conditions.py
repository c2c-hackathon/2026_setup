"""Component tests for Connect Four win and tie detection."""

import typing

import pytest

import tests._utils

VERTICAL_FIRST_COLUMN_ROWS = [
    "........",
    "........",
    "........",
    "P.......",
    "P.......",
    "P.......",
]


def seed_game(connect_four_module, game, rows, current_player):
    token_to_state = {
        ".": connect_four_module.CellState.EMPTY,
        "1": connect_four_module.CellState.PLAYER_1,
        "2": connect_four_module.CellState.PLAYER_2,
    }
    game.game_state = [[token_to_state[cell] for cell in row] for row in rows]
    game.current_player = current_player
    game.update_board_colors()
    game.show_current_player()


def materialize_rows(rows: typing.Iterable[str], player_token: str) -> typing.List[str]:
    opponent_token = "2" if player_token == "1" else "1"
    translation = str.maketrans({"P": player_token, "F": opponent_token})
    return [row.translate(translation) for row in rows]


def assert_end_game_controls(board):
    for column in range(7):
        assert board.callbacks[(column, 0)] is None
        assert board.color_at(column, 0) == (0, 0, 0)

    assert board.callbacks[(7, 0)] is not None
    assert board.color_at(7, 0) == (40, 255, 40)


@pytest.mark.parametrize("player_token", ["1", "2"], ids=["player_1", "player_2"])
def test___three_pieces_in_first_column___column_pressed___vertical_win_is_detected(
    connect_four_module,
    game_and_board,
    player_token,
):
    game, board = game_and_board
    current_player = tests._utils.player_state(connect_four_module, player_token)

    seed_game(
        connect_four_module,
        game,
        materialize_rows(VERTICAL_FIRST_COLUMN_ROWS, player_token),
        current_player,
    )

    board.press(0, 0)

    assert board.color_at(0, 4) == game.get_player_color(current_player)
    assert_end_game_controls(board)


VERTICAL_MIDDLE_COLUMN_ROWS = [
    "........",
    "........",
    "........",
    "....P...",
    "....P...",
    "....P...",
]


@pytest.mark.parametrize("player_token", ["1", "2"], ids=["player_1", "player_2"])
def test___three_pieces_in_middle_column___column_pressed___vertical_win_is_detected(
    connect_four_module,
    game_and_board,
    player_token,
):
    game, board = game_and_board
    current_player = tests._utils.player_state(connect_four_module, player_token)

    seed_game(
        connect_four_module,
        game,
        materialize_rows(VERTICAL_MIDDLE_COLUMN_ROWS, player_token),
        current_player,
    )

    board.press(4, 0)

    assert board.color_at(4, 4) == game.get_player_color(current_player)
    assert_end_game_controls(board)


HORIZONTAL_BOTTOM_ROW_ROWS = [
    "........",
    "........",
    "........",
    "........",
    "........",
    "PPP.....",
]


@pytest.mark.parametrize("player_token", ["1", "2"], ids=["player_1", "player_2"])
def test___three_bottom_row_pieces___adjacent_column_pressed___horizontal_bottom_row_win_is_detected(
    connect_four_module,
    game_and_board,
    player_token,
):
    game, board = game_and_board
    current_player = tests._utils.player_state(connect_four_module, player_token)

    seed_game(
        connect_four_module,
        game,
        materialize_rows(HORIZONTAL_BOTTOM_ROW_ROWS, player_token),
        current_player,
    )

    board.press(3, 0)

    assert board.color_at(3, 7) == game.get_player_color(current_player)
    assert_end_game_controls(board)


HORIZONTAL_MIDDLE_ROW_ROWS = [
    "........",
    "........",
    "........",
    "..PPP...",
    "..FPFP..",
    "..PFPF..",
]


@pytest.mark.parametrize("player_token", ["1", "2"], ids=["player_1", "player_2"])
def test___three_middle_row_pieces___supported_column_pressed___horizontal_middle_row_win_is_detected(
    connect_four_module,
    game_and_board,
    player_token,
):
    game, board = game_and_board
    current_player = tests._utils.player_state(connect_four_module, player_token)

    seed_game(
        connect_four_module,
        game,
        materialize_rows(HORIZONTAL_MIDDLE_ROW_ROWS, player_token),
        current_player,
    )

    board.press(5, 0)

    assert board.color_at(5, 5) == game.get_player_color(current_player)
    assert_end_game_controls(board)


DIAGONAL_CASES = [
    pytest.param(
        [
            "........",
            "........",
            "........",
            "FP......",
            "FFP.....",
            "FFFP....",
        ],
        0,
        2,
        0,
        id="descending-left-edge",
    ),
    pytest.param(
        [
            "........",
            "........",
            "...P....",
            "..PF....",
            ".PFF....",
            "PFFF....",
        ],
        3,
        2,
        3,
        id="ascending-left-edge",
    ),
    pytest.param(
        [
            "........",
            "........",
            "........",
            "..FP....",
            "..FFP...",
            "..FFFP..",
        ],
        2,
        2,
        2,
        id="descending-middle",
    ),
    pytest.param(
        [
            "........",
            "........",
            "....PF..",
            "...PFF..",
            "..PFFF..",
            "..FFFF..",
        ],
        5,
        1,
        5,
        id="ascending-middle",
    ),
]


@pytest.mark.parametrize("player_token", ["1", "2"], ids=["player_1", "player_2"])
@pytest.mark.parametrize("rows, move_column, expected_row, expected_column", DIAGONAL_CASES)
def test___three_diagonal_pieces___supported_column_pressed___diagonal_win_is_detected(
    connect_four_module,
    game_and_board,
    player_token,
    rows,
    move_column,
    expected_row,
    expected_column,
):
    game, board = game_and_board
    current_player = tests._utils.player_state(connect_four_module, player_token)

    seed_game(
        connect_four_module,
        game,
        materialize_rows(rows, player_token),
        current_player,
    )

    board.press(move_column, 0)

    assert board.color_at(
        expected_column, expected_row + connect_four_module.ROW_OFFSET
    ) == game.get_player_color(current_player)
    assert_end_game_controls(board)


TIE_ROWS = [
    "2211221.",
    "11221122",
    "22112211",
    "11221122",
    "22112211",
    "11221122",
]


def test___board_has_one_empty_cell_without_a_winner___final_column_pressed___tie_is_detected(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board

    seed_game(connect_four_module, game, TIE_ROWS, connect_four_module.CellState.PLAYER_1)

    board.press(7, 0)

    assert board.color_at(7, 2) == game.get_player_color(connect_four_module.CellState.PLAYER_1)
    assert_end_game_controls(board)
