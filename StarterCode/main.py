import time

from ConnectFour import ConnectFour
from NeoTrellisGame import NeoTrellisGame

game = ConnectFour()
game.game.update_display()
while True:
    try:
        game.game.sync()
        time.sleep(0.1)
    except KeyboardInterrupt:
        # clear board
        print("\nClosing game...")
        game.game.clear_board()
        exit()  # quit

