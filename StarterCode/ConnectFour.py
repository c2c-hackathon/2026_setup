from NeoTrellisGame import NeoTrellisGame

class ConnectFour(NeoTrellisGame):

    #GIVEN
    def __init__(self):
        super().__init__()
    

    def register_callbacks(self):
        pass


    def reset_game(self):
        pass

    
    def handle_button_event(self):
        pass


    def map_pressed_key_to_column(self):
        pass


    def find_lowest_empty_row(self, col: int):
        pass


    def drop_piece(self, col: int, player: int):
        pass


    def switch_player(self):
        pass


    def board_is_full(self) -> bool:
        pass


    def draw_board(self):
        pass


    def draw_cursor(self, col: int, player: int):
        pass


    def animate_piece_drop(self, col: int, player: int):
        pass


    def notify_column_is_full(self, col: int):
        pass


    def check_win(self, row: int, col: int, player: int):
        pass


    def count_in_direction(self, col: int, d_row: int, d_col: int):
        pass


    def count_one_side(self, row: int, col: int, d_row: int, d_col: int):
        pass 


    def get_winning_cells(self, player: int):
        pass


    def highlight_winning_sequence(self, cells: list[tuple(int, int)]):
        pass


    def show_winner(self, player: int):
        pass


    def show_draw(self):
        pass

    def get_other_player(self) -> int:
        pass






