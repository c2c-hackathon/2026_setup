"""Solve a Connect Four board into a legal move sequence.

Edit GAME_STATE to the target board you want to reproduce. The script prints
the alternating P/F moves needed to reach that state from an empty board, or
reports why the state is unreachable.
"""

import typing

ROWS = 6
COLUMNS = 8
CONNECT_LENGTH = 4
EMPTY = "."
PLAYER = "P"
FOLLOWER = "F"
TOKENS = {EMPTY, PLAYER, FOLLOWER}

GAME_STATE = [
    "........",
    "........",
    "........",
    "....FP..",
    "....PFP.",
    "P...FFFP",
]

STARTING_PLAYER = PLAYER

Board = tuple[str, ...]
Move = tuple[str, int]


def normalize_board(rows: typing.Sequence[str]) -> Board:
    if len(rows) != ROWS:
        raise ValueError("GAME_STATE must contain exactly %s rows" % ROWS)

    normalized_rows = []
    for row_index, row in enumerate(rows):
        if len(row) != COLUMNS:
            raise ValueError(
                "GAME_STATE row %s must contain exactly %s columns" % (row_index, COLUMNS)
            )
        invalid_tokens = sorted(set(row) - TOKENS)
        if invalid_tokens:
            raise ValueError(
                "GAME_STATE row %s contains invalid token(s): %s"
                % (row_index, ", ".join(invalid_tokens))
            )
        normalized_rows.append(row)

    board = tuple(normalized_rows)
    validate_gravity(board)
    validate_turn_counts(board)
    validate_winner_consistency(board)
    return board


def validate_gravity(board: Board) -> None:
    for column in range(COLUMNS):
        found_empty = False
        for row in range(ROWS - 1, -1, -1):
            cell = board[row][column]
            if cell == EMPTY:
                found_empty = True
            else:
                if found_empty:
                    raise ValueError(
                        "Column %s violates gravity: checker above an empty cell" % column
                    )


def count_tokens(board: Board) -> dict[str, int]:
    counts = {PLAYER: 0, FOLLOWER: 0}
    for row in board:
        for cell in row:
            if cell in counts:
                counts[cell] += 1
    return counts


def other_player(player: str) -> str:
    return FOLLOWER if player == PLAYER else PLAYER


def validate_turn_counts(board: Board) -> None:
    counts = count_tokens(board)
    first_count = counts[STARTING_PLAYER]
    second_count = counts[other_player(STARTING_PLAYER)]

    if first_count < second_count:
        raise ValueError("Second player cannot have more moves than the starter")
    if first_count - second_count > 1:
        raise ValueError("Starter cannot be more than one move ahead")


def has_winning_line(board: Board, player: str) -> bool:
    directions = ((0, 1), (1, 0), (1, 1), (1, -1))

    for row in range(ROWS):
        for column in range(COLUMNS):
            if board[row][column] != player:
                continue

            for row_step, column_step in directions:
                if all(
                    0 <= row + row_step * offset < ROWS
                    and 0 <= column + column_step * offset < COLUMNS
                    and board[row + row_step * offset][column + column_step * offset] == player
                    for offset in range(CONNECT_LENGTH)
                ):
                    return True

    return False


def validate_winner_consistency(board: Board) -> None:
    player_wins = has_winning_line(board, PLAYER)
    follower_wins = has_winning_line(board, FOLLOWER)
    if player_wins and follower_wins:
        raise ValueError("Both players cannot already have a winning line")


def next_player(board: Board) -> str:
    counts = count_tokens(board)
    if counts[STARTING_PLAYER] == counts[other_player(STARTING_PLAYER)]:
        return STARTING_PLAYER
    return other_player(STARTING_PLAYER)


def player_who_moved_last(board: Board) -> str | None:
    total_moves = sum(count_tokens(board).values())
    if total_moves == 0:
        return None
    return other_player(next_player(board))


def topmost_checker_row(board: Board, column: int) -> int | None:
    for row in range(ROWS):
        if board[row][column] != EMPTY:
            return row
    return None


def remove_checker(board: Board, row: int, column: int) -> Board:
    mutable_rows = [list(board_row) for board_row in board]
    mutable_rows[row][column] = EMPTY
    return tuple("".join(board_row) for board_row in mutable_rows)


def previous_board_is_playable(board: Board) -> bool:
    return not has_winning_line(board, PLAYER) and not has_winning_line(board, FOLLOWER)


def solve_board(board: Board) -> list[Move] | None:
    memo: dict[tuple[Board, str | None], list[Move] | None] = {}
    return solve_board_recursive(board, player_who_moved_last(board), memo)


def solve_board_recursive(
    board: Board,
    expected_last_player: str | None,
    memo: dict[tuple[Board, str | None], list[Move] | None],
) -> list[Move] | None:
    memo_key = (board, expected_last_player)
    if memo_key in memo:
        return memo[memo_key]

    if expected_last_player is None:
        if all(row == EMPTY * COLUMNS for row in board):
            return []
        memo[memo_key] = None
        return None

    for column in range(COLUMNS):
        row = topmost_checker_row(board, column)
        if row is None:
            continue
        if board[row][column] != expected_last_player:
            continue

        previous_board = remove_checker(board, row, column)
        if not previous_board_is_playable(previous_board):
            continue

        solution_prefix = solve_board_recursive(
            previous_board,
            player_who_moved_last(previous_board),
            memo,
        )
        if solution_prefix is None:
            continue

        solution = solution_prefix + [(expected_last_player, column)]
        memo[memo_key] = solution
        return solution

    memo[memo_key] = None
    return None


def drop_piece(board: Board, column: int, player: str) -> tuple[Board, int]:
    mutable_rows = [list(row) for row in board]
    for row in range(ROWS - 1, -1, -1):
        if mutable_rows[row][column] == EMPTY:
            mutable_rows[row][column] = player
            return tuple("".join(current_row) for current_row in mutable_rows), row
    raise ValueError("Column %s is full" % column)


def format_board(board: Board) -> str:
    return "\n".join(board)


def main() -> int:
    board = normalize_board(GAME_STATE)
    solution = solve_board(board)

    print("Target board:")
    print(format_board(board))
    print()

    if solution is None:
        print("No legal alternating move sequence reaches this board.")
        return 1

    print("Solved in %s move(s):" % len(solution))
    print("MOVES = %s" % [column for _, column in solution])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
