import board
import busio
import digitalio
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis


class NeoTrellisGame:
    
    def __init__(self):
        self.init_hardware()

    #GIVEN
    def init_hardware(self):
        print("Initializing Hardware")
        i2c_bus = busio.I2C(board.SCL, board.SDA)

        self.__boards = [
            [NeoTrellis(i2c_bus, False, addr=0x2E, auto_write=False), NeoTrellis(i2c_bus, False, addr=0x2F, auto_write=False)],
            [NeoTrellis(i2c_bus, False, addr=0x30, auto_write=False), NeoTrellis(i2c_bus, False, addr=0x31, auto_write=False)],
            ]
        self.board = MultiTrellis(self.__boards)
        print("Hardware is ready")
  
    #GIVEN
    #An alternative is to let them register callbacks with the registerCallback(x, y, callback) instead of the index based one
    def key_index_to_xy_coordinates(self, index: int) -> tuple[int, int]:
        if index < 0 or index > 63:
            raise ValueError(f"Index must be between 0 and 63 inclusive. Was {index}")
        else:
            x = int(index / 8)
            y = int(index % 8)
            return x, y
      
    #GIVEN
    def xy_coordinates_to_key_index(self, x: int, y: int) -> int:
        self.validate_coordinates(x,y)
        return (x * 8) + y
    
    #GIVEN
    def validate_coordinates(self, x: int, y: int):
        if x < 0 or x > 7:
            raise ValueError(f"X coordinate must be between 0 and 7 inclusive. Was {x}") 
        
        if y < 0 or y > 7:
            raise ValueError(f"Y coordinate must be between 0 and 7 inclusive. Was {y}") 
    
    #GIVEN
    def set_cell_color(self, x: int, y: int, color: tuple[int, int, int]) -> None:
        self.validate_coordinates(x, y)
        for rbgValue in color:
            if rbgValue < 0 or rbgValue > 255:
                raise ValueError(f"All RGB values in the color must be between 0 and 255 inclusive. Was {color}")
        self.board.color(x, y, color)
    
    #GIVEN
    def update_display(self):
        self.board.show()

    def clear_board(self):
        """Clears board by turning off all LEDs"""
        for x in range(8):
            for y in range(8):
                self.set_cell_color(x, y, [0, 0, 0])
        self.update_display()

