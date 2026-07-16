from ConnectFour import ConnectFour
from NeoTrellisGame import NeoTrellisGame
import time


game = ConnectFour()
game.update_display()
while True:
    game.board.sync()
    pass