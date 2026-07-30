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
        for x in range(8):
            for y in range(8):
                game.set_cell_color(x, y, [0, 0, 0])
        game.update_display()
        exit()  # quit

