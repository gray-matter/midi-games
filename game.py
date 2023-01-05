import re
from datetime import timedelta

from effect.snake_effect import SnakeEffect
from game.whack_a_mole import WhackAMole
from grid.pad_grid import PadGrid
from midi.midi_controller import MidiController


def main():
    ctrl = MidiController(re.compile('LPD8'))
    ctrl.connect()
    pad_grid = PadGrid(ctrl, [45, 46, 47, 48, 41, 42, 43, 44], 4, 2)

    try:
        snake = SnakeEffect(pad_grid, ctrl, 3, timedelta(seconds=0.2), 2)
        snake.play()

        g = WhackAMole(pad_grid, ctrl, timedelta(seconds=0.5), 5)
        print(g.play())
    finally:
        pad_grid.reset(ctrl)


main()
