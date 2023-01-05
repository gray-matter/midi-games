from typing import List

from midi.midi_controller import MidiController


class PadGrid:
    def __init__(self, controller: MidiController, notes: List[int], width: int, height: int):
        self._controller = controller
        self.width = width
        self.height = height
        self._notes = notes

    def get_note(self, x: int, y: int) -> int:
        return self._notes[y * self.width + x]

    def all_notes(self) -> List[int]:
        return [self.get_note(x, y) for y in range(self.height) for x in range(self.width)]
