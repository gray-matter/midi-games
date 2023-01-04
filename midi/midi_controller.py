import logging
import re
from typing import List, Optional

import mido
from mido import Message
from mido.backends.rtmidi import Input, Output


class MidiController:
    def __init__(self, name_regex: re.Pattern):
        self._outport: Optional[Output] = None
        self._inport: Optional[Input] = None
        self._name_regex = name_regex

    def connect(self) -> bool:
        inport_name = self._find(mido.get_input_names())
        outport_name = self._find(mido.get_output_names())

        if inport_name:
            self._inport = mido.open_input(inport_name)

        if outport_name:
            self._outport = mido.open_output(outport_name)

        return self._inport and self._outport

    def _find(self, available: List[str]) -> Optional[str]:
        matching = [dev_name for dev_name in set(available) if self._name_regex.search(dev_name)]

        if len(matching) == 0:
            logging.warning(f'Could not find device matching "{self._name_regex.pattern}" '
                            f'(available devices: {available}')
            return None

        if len(matching) > 1:
            logging.warning(f'More than 1 device matched "{self._name_regex.pattern}" (available devices: {available}, '
                            f'picking first')

        return matching[0]

    def note_on(self, note: int):
        msg = Message('note_on', note=note)
        self._outport.send(msg)

    def note_off(self, note: int):
        msg = Message('note_off', note=note)
        self._outport.send(msg)
