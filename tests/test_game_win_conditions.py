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


@pytest.fixture
def seeded_game(connect_four_module, game_and_board):
    game, board = game_and_board

    def _seeded_game(rows, player_token):
        current_player = tests._utils.player_state(connect_four_module, player_token)
        seed_game(
            connect_four_module,
            game,
            materialize_rows(rows, player_token),
            current_player,
        )
        return game, board, current_player

    return _seeded_game


def assert_end_game_controls(connect_four_module, board):
    for column in range(7):
        assert board.color_at(column, 0) == (0, 0, 0)

    assert board.callbacks[(7, 0)] is not None
    assert board.color_at(7, 0) == connect_four_module.HIGHLIGHT_COLOR


@pytest.mark.parametrize("player_token", ["1", "2"], ids=["player_1", "player_2"])
def test___three_pieces_in_first_column___column_pressed___vertical_win_is_detected(
    connect_four_module,
    seeded_game,
    player_token,
):
    game, board, current_player = seeded_game(VERTICAL_FIRST_COLUMN_ROWS, player_token)

    board.press(0, 0)

    assert board.color_at(0, 4) == game.get_player_color(current_player)
    assert_end_game_controls(connect_four_module, board)

# moves: MOVES = [4, 3, 4, 3, 4, 3]
VERTICAL_MIDDLE_COLUMN_ROWS = [
    "........",
    "........",
    "........",
    "...FP...",
    "...FP...",
    "...FP...",
]


@pytest.mark.parametrize("player_token", ["1", "2"], ids=["player_1", "player_2"])
def test___three_pieces_in_middle_column___column_pressed___vertical_win_is_detected(
    connect_four_module,
    seeded_game,
    player_token,
):
    game, board, current_player = seeded_game(VERTICAL_MIDDLE_COLUMN_ROWS, player_token)

    board.press(4, 0)

    assert board.color_at(4, 4) == game.get_player_color(current_player)
    assert_end_game_controls(connect_four_module, board)


# moves: MOVES = [2, 7, 1, 6, 0, 5]
HORIZONTAL_BOTTOM_ROW_ROWS = [
    "........",
    "........",
    "........",
    "........",
    "........",
    "PPP..FFF",
]


@pytest.mark.parametrize("player_token", ["1", "2"], ids=["player_1", "player_2"])
def test___three_bottom_row_pieces___adjacent_column_pressed___horizontal_bottom_row_win_is_detected(
    connect_four_module,
    seeded_game,
    player_token,
):
    game, board, current_player = seeded_game(HORIZONTAL_BOTTOM_ROW_ROWS, player_token)

    board.press(3, 0)

    assert board.color_at(3, 7) == game.get_player_color(current_player)
    assert_end_game_controls(connect_four_module, board)


# moves: MOVES = [4, 5, 5, 4, 4, 3, 2, 2, 3, 1, 3, 1, 2]
HORIZONTAL_MIDDLE_ROW_ROWS = [
    "........",
    "........",
    "........",
    "..PPP...",
    ".FFPFP..",
    ".FPFPF..",
]


@pytest.mark.parametrize("player_token", ["1", "2"], ids=["player_1", "player_2"])
def test___three_middle_row_pieces___supported_column_pressed___horizontal_middle_row_win_is_detected(
    connect_four_module,
    seeded_game,
    player_token,
):
    game, board, current_player = seeded_game(HORIZONTAL_MIDDLE_ROW_ROWS, player_token)

    board.press(5, 0)

    assert board.color_at(5, 5) == game.get_player_color(current_player)
    assert_end_game_controls(connect_four_module, board)


DIAGONAL_CASES = [
    # moves: MOVES = [7, 2, 1, 1, 3, 0, 2, 0, 1, 0]
    pytest.param(
        [
            "........",
            "........",
            "........",
            "FP......",
            "FFP.....",
            "FPFP...P",
        ],
        0,
        2,
        0,
        id="descending-left-edge",
    ),
    # moves: MOVES = [7, 3, 7, 2, 6, 2, 2, 1, 1, 3, 0, 3]
    pytest.param(
        [
            "........",
            "........",
            "........",
            "..PF...P",
            ".PFF...P",
            "PFFF...P",
        ],
        3,
        2,
        3,
        id="ascending-left-edge",
    ),
    # moves: MOVES = [7, 4, 7, 3, 7, 3, 5, 2, 4, 2, 3, 2]
    pytest.param(
        [
            "........",
            "........",
            "........",
            "..FP...P",
            "..FFP..P",
            "..FFFP.P",
        ],
        2,
        2,
        2,
        id="descending-middle",
    ),
    # moves: MOVES = [7, 6, 6, 5, 0, 5, 5, 4, 0, 4, 0, 4]
    pytest.param(
        [
            "........",
            "........",
            "........",
            "....FP..",
            "....FFP.",
            "....FFFP",
        ],
        4,
        2,
        4,
        id="descending-right-edge",
    ),
    # moves: MOVES = [7, 4, 7, 4, 7, 4, 5, 3, 4, 3, 3, 2, 2, 5, 0, 5, 0, 5]
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
    seeded_game,
    player_token,
    rows,
    move_column,
    expected_row,
    expected_column,
):
    game, board, current_player = seeded_game(rows, player_token)

    board.press(move_column, 0)

    assert board.color_at(
        expected_column, expected_row + connect_four_module.ROW_OFFSET
    ) == game.get_player_color(current_player)
    assert_end_game_controls(connect_four_module, board)

# moves: Moves = MOVES = [7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 7, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 4, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
TIE_ROWS = [
    "PPFFPPF.",
    "FFPPFFPP",
    "PPFFPPFF",
    "FFPPFFPP",
    "PPFFPPFF",
    "FFPPFFPP",
]


@pytest.mark.parametrize("current_player", ["1", "2"], ids=["player_1", "player_2"])
def test___board_has_one_empty_cell_without_a_winner___final_column_pressed___tie_is_detected(
    current_player,
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board

    current_player_state = tests._utils.player_state(connect_four_module, current_player)
    seed_game(
        connect_four_module,
        game,
        materialize_rows(TIE_ROWS, current_player),
        current_player_state,
    )

    board.press(7, 0)

    assert board.color_at(7, 2) == game.get_player_color(current_player_state)
    assert_end_game_controls(connect_four_module, board)
