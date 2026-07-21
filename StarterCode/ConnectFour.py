from NeoTrellisGame import NeoTrellisGame
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis #TODO: Make this import better


# Represents the state of the board in the game_state matrix
EMPTY = -1
PLAYER_1 = 0
PLAYER_2 = 1

# Row is the NeoTrellis Y and Col is the NeoTrellis X
NUMBER_OF_GAME_ROWS = 6
NUMBER_OF_GAME_COLUMNS = 8
ROW_OFFSET = 8 - NUMBER_OF_GAME_ROWS
NUMBER_TO_WIN = 4

class ConnectFour(NeoTrellisGame):

    def __init__(self):
        super().__init__()
        self.reset_game()
        self.register_two_player_callbacks()
    

    def register_two_player_callbacks(self):
        for col in range(NUMBER_OF_GAME_COLUMNS):
            self.board.set_callback(col, 0, self.handle_button_event)
            self.board.activate_key(col, 0, NeoTrellis.EDGE_RISING)


    def register_end_game_callbacks(self):
        for col in range(NUMBER_OF_GAME_COLUMNS):
            self.board.set_callback(col, 0, None)
        self.board.set_callback(7, 0, self.reset_game_from_callback)


    def register_callbacks(self):
        pass
    
    def reset_game_from_callback(self, x, y, edge):
        self.reset_game()
        self.register_two_player_callbacks()

    def reset_game(self):
        self.game_state = [] # Zero indexed: Row, Column
        self.current_player = PLAYER_1

        for i in range(NUMBER_OF_GAME_ROWS):
            self.game_state.append([EMPTY] * NUMBER_OF_GAME_COLUMNS)
        self.show_current_player()
        self.update_board_colors()

    
    def handle_button_event(self, x, y, edge):
        if not self.is_column_full(x):
            self.drop_piece(x, self.current_player)


    def find_lowest_empty_row(self, col: int):
        for row_index in range(NUMBER_OF_GAME_ROWS):
            if self.game_state[NUMBER_OF_GAME_ROWS - row_index - 1][col] == EMPTY:
                return NUMBER_OF_GAME_ROWS - row_index - 1
        return -1 # -1 means the column is full


    def drop_piece(self, col: int, player: int):
        self.game_state[self.find_lowest_empty_row(col)][col] = self.current_player
        self.update_board_colors()
        win, winning_sequence = self.check_win()
        tie = self.board_is_full() 
        if not win and not tie:
            self.switch_player()
        elif win:
            self.show_winner(winning_sequence) 
        else:
            self.show_tie_game()

    def switch_player(self):
        if self.current_player == PLAYER_1:
            self.current_player = PLAYER_2
        else:
            self.current_player = PLAYER_1

        self.show_current_player()


    def show_current_player(self):
        for col in range(NUMBER_OF_GAME_COLUMNS):
            self.set_cell_color(col, 0, self.get_player_color(self.current_player))
        self.update_display()


    def board_is_full(self) -> bool:
        for col in range(NUMBER_OF_GAME_COLUMNS):
            if not self.is_column_full(col):
                return False

        return True


    def update_board_colors(self):
        for row_index, row in enumerate(self.game_state):
            for col_index, col in enumerate(row):

                self.set_cell_color(col_index, row_index + ROW_OFFSET, self.get_player_color(col))
        self.update_display()


    def get_player_color(self, player: int):
        if player == PLAYER_1:
            return (255, 40, 40)
        elif player == PLAYER_2:
            return (40, 40, 255)
        else:
            return (50, 50, 50)


    def animate_piece_drop(self, col: int, player: int):
        pass

    

    def is_column_full(self, col: int) -> bool:
        for row in self.game_state:
            if row[col] == EMPTY:
                return False
        return True

    
    def check_for_horizontal_win(self, row, col):
        current_col = col
        cells = []
        while len(cells) <=NUMBER_TO_WIN and current_col < NUMBER_OF_GAME_COLUMNS:
            if self.game_state[row][current_col] == self.current_player:
                cells.append((row, current_col))
                current_col += 1
            else:
                break
        return cells


    def check_for_vertical_win(self, row, col):
        current_row = row
        cells = []
        while len(cells) <=NUMBER_TO_WIN and current_row < NUMBER_OF_GAME_ROWS:
            if self.game_state[current_row][col] == self.current_player:
                cells.append((current_row, col))
                current_row += 1
            else:
                break
        return cells

    
    def check_for_diagonal_win_1(self, row, col):
        current_row = row
        current_col = col
        cells = []
        while len(cells) <=NUMBER_TO_WIN and current_row < NUMBER_OF_GAME_ROWS and current_col < NUMBER_OF_GAME_COLUMNS:
            if self.game_state[current_row][current_col] == self.current_player:
                cells.append((current_row, current_col))
                current_row += 1
                current_col += 1
            else:
                break
        return cells

    
    def check_for_diagonal_win_2(self, row, col):
        current_row = row
        current_col = col
        cells = []
        while len(cells) <=NUMBER_TO_WIN and current_row >= 0 and current_col < NUMBER_OF_GAME_COLUMNS:
            if self.game_state[current_row][current_col] == self.current_player:
                cells.append((current_row, current_col))
                current_row -= 1
                current_col += 1
            else:
                break
        return cells


    def check_win(self):
        win_checkers = [self.check_for_horizontal_win, self.check_for_vertical_win, self.check_for_diagonal_win_1, self.check_for_diagonal_win_2]
        for row_index in range(NUMBER_OF_GAME_ROWS):
            for col_index in range(NUMBER_OF_GAME_COLUMNS):
                if self.game_state[row_index][col_index] == self.current_player:
                    for f in win_checkers:
                        longest_sequence = f(row_index, col_index)
                        if len(longest_sequence) >= NUMBER_TO_WIN: 
                            return True, longest_sequence
        return False, []


    def get_winning_cells(self):
        pass

    def blink_board(self):
        for i in range(10):
            for row in range(NUMBER_OF_GAME_ROWS):
                for col in range(NUMBER_OF_GAME_COLUMNS):
                    self.set_cell_color(col, row + ROW_OFFSET, (0,0,0))
                self.update_display()

            for row in range(NUMBER_OF_GAME_ROWS):
                for col in range(NUMBER_OF_GAME_COLUMNS):
                    self.set_cell_color(col, row + ROW_OFFSET, self.get_player_color(self.game_state[row][col]))
                self.update_display()

    def highlight_winning_sequence(self, cells):
        for i in range(10):
            for cell in cells:
                self.set_cell_color(cell[1], cell[0] + ROW_OFFSET, (40, 255, 40))
                self.update_display()
            for cell in cells:
                self.set_cell_color(cell[1], cell[0] + ROW_OFFSET, self.get_player_color(self.current_player))
                self.update_display()


    def show_winner(self, winning_sequence):
        self.register_end_game_callbacks()
        for col in range(NUMBER_OF_GAME_COLUMNS):
            self.set_cell_color(col, 0, (0, 0, 0))
        self.set_cell_color(7, 0, (40, 255, 40))
        self.highlight_winning_sequence(winning_sequence)    


    def show_tie_game(self):
        self.register_end_game_callbacks()
        for col in range(NUMBER_OF_GAME_COLUMNS):
            self.set_cell_color(col, 0, (0, 0, 0))
        self.set_cell_color(7, 0, (40, 255, 40))
        self.blink_board()






