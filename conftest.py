"""Pytest startup adjustments and shared Connect Four test helpers."""

import importlib
import importlib.util
import pathlib
import sys
import sysconfig
import types

import pytest


def _load_stdlib_code_module() -> None:
    if "code" in sys.modules:
        return

    stdlib_path = pathlib.Path(sysconfig.get_path("stdlib")) / "code.py"
    spec = importlib.util.spec_from_file_location("code", stdlib_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load stdlib code module from {stdlib_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["code"] = module
    spec.loader.exec_module(module)


_load_stdlib_code_module()


class FakeNeoTrellisGame:
    """Fake board implementation used to exercise Connect Four without hardware."""

    def __init__(self):
        self.callbacks = {}
        self.colors = {}
        self.display_updates = 0
        self.key_states = {}

    def init_hardware(self):
        return None

    def set_cell_color(self, x, y, color):
        self.colors[(x, y)] = color

    def update_display(self):
        self.display_updates += 1

    def clear_board(self):
        self.colors.clear()

    def sync(self):
        return None

    def set_callback(self, x, y, callback):
        self.callbacks[(x, y)] = callback

    def activate_key(self, x, y, edge, enable=True):
        self.key_states[(x, y)] = {"edge": edge, "enable": enable}

    def press(self, x, y):
        """Trigger a registered key callback when that key is enabled."""
        callback = self.callbacks.get((x, y))
        key_state = self.key_states.get((x, y), {"enable": True, "edge": None})
        if callback is None or not key_state["enable"]:
            return False

        callback(x, y, key_state["edge"])
        return True

    def color_at(self, x, y):
        return self.colors[(x, y)]


def _install_fake_hardware_modules():
    board_module = types.ModuleType("board")
    setattr(board_module, "SCL", object())
    setattr(board_module, "SDA", object())
    sys.modules["board"] = board_module

    busio_module = types.ModuleType("busio")

    class _FakeI2C:
        def __init__(self, *_args, **_kwargs):
            pass

    setattr(busio_module, "I2C", _FakeI2C)
    sys.modules["busio"] = busio_module
    sys.modules["digitalio"] = types.ModuleType("digitalio")

    adafruit_package = types.ModuleType("adafruit_neotrellis")
    multitrellis_module = types.ModuleType("adafruit_neotrellis.multitrellis")
    neotrellis_module = types.ModuleType("adafruit_neotrellis.neotrellis")

    class _FakeMultiTrellis:
        def __init__(self, *_args, **_kwargs):
            pass

        def color(self, *_args, **_kwargs):
            pass

        def show(self):
            pass

        def sync(self):
            pass

        def set_callback(self, *_args, **_kwargs):
            pass

        def activate_key(self, *_args, **_kwargs):
            pass

    class _FakeNeoTrellis:
        EDGE_RISING = object()

        def __init__(self, *_args, **_kwargs):
            pass

    setattr(multitrellis_module, "MultiTrellis", _FakeMultiTrellis)
    setattr(neotrellis_module, "NeoTrellis", _FakeNeoTrellis)
    setattr(adafruit_package, "multitrellis", multitrellis_module)
    setattr(adafruit_package, "neotrellis", neotrellis_module)

    sys.modules["adafruit_neotrellis"] = adafruit_package
    sys.modules["adafruit_neotrellis.multitrellis"] = multitrellis_module
    sys.modules["adafruit_neotrellis.neotrellis"] = neotrellis_module


@pytest.fixture(scope="session")
def connect_four_module():
    _install_fake_hardware_modules()

    starter_code_path = pathlib.Path(__file__).resolve().parent / "StarterCode"
    if str(starter_code_path) not in sys.path:
        sys.path.insert(0, str(starter_code_path))

    sys.modules.pop("ConnectFour", None)
    sys.modules.pop("NeoTrellisGame", None)
    return importlib.import_module("ConnectFour")


@pytest.fixture
def game_and_board(connect_four_module):
    board = FakeNeoTrellisGame()
    game = connect_four_module.ConnectFour(game=board)
    return game, board
