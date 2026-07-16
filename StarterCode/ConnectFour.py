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

class ConnectFour(NeoTrellisGame):

    def __init__(self):
        super().__init__()
        self.reset_game()
        self.register_callbacks()
    

    def register_callbacks(self):
        for col in range(NUMBER_OF_GAME_COLUMNS):
            self.board.set_callback(col, 0, self.handle_button_event)
            self.board.activate_key(col, 0, NeoTrellis.EDGE_RISING)


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
        win = self.check_win()
        tie = self.board_is_full() 
        if not win and not tie:
            self.switch_player()
        elif win:
            print(f"Winner! {self.current_player}")        
        else:
            print(f"Tie game!")


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
        count = 0
        current_col = col
        while count <=4 and current_col < NUMBER_OF_GAME_COLUMNS:
            if self.game_state[row][current_col] == self.current_player:
                count += 1
                current_col += 1
            else:
                break
        return count >= 4


    def check_for_vertical_win(self, row, col):
        count = 0
        current_row = row
        while count <=4 and current_row < NUMBER_OF_GAME_ROWS:
            if self.game_state[current_row][col] == self.current_player:
                count += 1
                current_row += 1
            else:
                break
        return count >= 4

    
    def check_for_diagonal_win_1(self, row, col):
        count = 0
        current_row = row
        current_col = col
        while count <=4 and current_row < NUMBER_OF_GAME_ROWS and current_col < NUMBER_OF_GAME_COLUMNS:
            if self.game_state[current_row][current_col] == self.current_player:
                count += 1
                current_row += 1
                current_col += 1
            else:
                break
        return count >= 4

    
    def check_for_diagonal_win_2(self, row, col):
        count = 0
        current_row = row
        current_col = col
        while count <=4 and current_row >= 0 and current_col < NUMBER_OF_GAME_COLUMNS:
            if self.game_state[current_row][current_col] == self.current_player:
                count += 1
                current_row -= 1
                current_col += 1
            else:
                break
        return count >= 4


    def check_win(self):
        for row_index in range(NUMBER_OF_GAME_ROWS):
            for col_index in range(NUMBER_OF_GAME_COLUMNS):
                if self.game_state[row_index][col_index] == self.current_player:
                    if self.check_for_horizontal_win(row_index, col_index) or self.check_for_vertical_win(row_index, col_index) or self.check_for_diagonal_win_1(row_index, col_index) or self.check_for_diagonal_win_2(row_index, col_index):

                        return True
        return False


    def get_winning_cells(self, player: int):
        pass


    def highlight_winning_sequence(self, cells):
        pass


    def show_winner(self, player: int):
        pass


    def show_tie_game(self):
        pass






