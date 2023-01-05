import asyncio
import random
from datetime import timedelta
from threading import Thread, Event
from typing import Callable, Coroutine

from mido import Message

from grid.pad_grid import PadGrid
from midi.midi_controller import MidiController


class WhackAMole:
    def __init__(self, pad_grid: PadGrid, controller: MidiController, base_delay: timedelta, max_hits: int):
        self._pad_grid = pad_grid
        self._controller = controller
        self._base_delay = base_delay
        self._max_hits = max_hits

    def play(self) -> int:
        current_x = 0
        current_y = 0
        nb_hits = 0
        stop_event = Event()

        def sync_loop(call: Callable[[], Coroutine]):
            asyncio.run(call())

        async def strokes_loop():
            async def handle_stroke(msg: Message):
                nonlocal nb_hits

                coord = self._pad_grid.note_coordinate(msg.note)
                if coord == (current_x, current_y):
                    nb_hits += 1

            [self._controller.bind_note_on(note, handle_stroke) for note in self._pad_grid.all_notes()]

            await self._controller.receive(stop_event)

        async def moles_loop():
            nonlocal current_x
            nonlocal current_y
            sent_hits = 0
            previous_x = -1
            previous_y = -1

            while sent_hits < self._max_hits:
                candidate_x = previous_x
                candidate_y = previous_y
                while candidate_x == previous_x and candidate_y == previous_y:
                    candidate_x = random.randint(0, self._pad_grid.width - 1)
                    candidate_y = random.randint(0, self._pad_grid.height - 1)

                previous_x = current_x = candidate_x
                previous_y = current_y = candidate_y
                self._controller.send_note_on(self._pad_grid.get_note(current_x, current_y))

                # Add a random delay
                delay = random.randint(-500, 200)
                await asyncio.sleep((self._base_delay + timedelta(milliseconds=delay)).total_seconds())
                self._controller.send_note_off(self._pad_grid.get_note(current_x, current_y))

                # Set to -1 to avoid hits to be counted during waiting time
                current_x = -1
                current_y = -1

                sent_hits += 1

                await asyncio.sleep(random.randint(1, 4))

        moles_thread = Thread(target=lambda: sync_loop(moles_loop))
        strokes_thread = Thread(target=lambda: sync_loop(strokes_loop))

        self._pad_grid.reset(self._controller)
        strokes_thread.start()
        moles_thread.start()

        moles_thread.join()
        stop_event.set()
        strokes_thread.join()
        self._pad_grid.reset(self._controller)

        return nb_hits
