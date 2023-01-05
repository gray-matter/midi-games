import re
from datetime import timedelta

from effect.snake_effect import SnakeEffect
from grid.pad_grid import PadGrid
from midi.midi_controller import MidiController


def main():
    ctrl = MidiController(re.compile('LPD8'))
    ctrl.connect()
    pad_grid = PadGrid(ctrl, [45, 46, 47, 48, 41, 42, 43, 44], 4, 2)

    try:
        [ctrl.send_note_off(note) for note in pad_grid.all_notes()]
        fx = SnakeEffect(pad_grid, ctrl, 3, timedelta(milliseconds=100))
        fx.play()
    finally:
        [ctrl.send_note_off(note) for note in pad_grid.all_notes()]


main()
