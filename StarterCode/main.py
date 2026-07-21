from ConnectFour import ConnectFour
from NeoTrellisGame import NeoTrellisGame

game = ConnectFour()
game.update_display()
while True:
    game.board.sync()
    pass
