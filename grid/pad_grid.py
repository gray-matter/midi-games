from typing import List

from midi.midi_controller import MidiController


class PadGrid:
    def __init__(self, controller: MidiController, notes: List[int], width: int, height: int):
        self._controller = controller
        self.width = width
        self.height = height
        self._notes = notes

    def light_on(self, x: int, y: int):
        note = self._get_note(x, y)
        self._controller.note_on(note)

    def light_off(self, x: int, y: int):
        note = self._get_note(x, y)
        self._controller.note_off(note)

    def _get_note(self, x: int, y: int) -> int:
        return self._notes[y * self.width + x]

    def light_on_all(self):
        for y in range(self.height):
            for x in range(self.width):
                self.light_on(x, y)

    def light_off_all(self):
        for y in range(self.height):
            for x in range(self.width):
                self.light_off(x, y)
