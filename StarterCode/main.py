from ConnectFour import ConnectFour
from NeoTrellisGame import NeoTrellisGame

game = ConnectFour()
game.update_display()
while True:
    try:
        game.board.sync()
    except KeyboardInterrupt:
        # clear board
        print("\nClosing game...")
        game.clear_board()
        exit()  # quit

