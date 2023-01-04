import enum
import time
from collections import deque
from datetime import timedelta

from grid.pad_grid import PadGrid


class HorizontalDirection(enum.Enum):
    LEFT = -1
    RIGHT = 1

    @staticmethod
    def reverse(direction: 'HorizontalDirection') -> 'HorizontalDirection':
        return HorizontalDirection(-int(direction.value))


class VerticalDirection(enum.Enum):
    UP = -1
    DOWN = 1

    @staticmethod
    def reverse(direction: 'VerticalDirection') -> 'VerticalDirection':
        return VerticalDirection(-int(direction.value))


class SnakeEffect:
    def __init__(self, pad_grid: PadGrid, length: int, delay: timedelta):
        self._pad_grid = pad_grid
        self._length = length
        self._delay = delay

    def play(self):
        current_vector = (-1, 0, HorizontalDirection.RIGHT, VerticalDirection.DOWN)
        rings = deque(maxlen=self._length)

        while True:
            next_vector = self._next_position(current_vector[0], current_vector[1],
                                              current_vector[2], current_vector[3])

            if len(rings) == rings.maxlen:
                self._pad_grid.light_off(rings[0][0], rings[0][1])

            rings.append(next_vector)
            self._pad_grid.light_on(next_vector[0], next_vector[1])
            current_vector = next_vector
            time.sleep(self._delay.microseconds / 1000. / 1000.)

    def _next_position(self, x: int, y: int,
                       horizontal_direction: HorizontalDirection,
                       vertical_direction: VerticalDirection) -> \
            tuple[int, int, HorizontalDirection, VerticalDirection]:
        next_x = x + horizontal_direction.value

        # Can move horizontally
        if self._pad_grid.width > next_x >= 0:
            return next_x, y, horizontal_direction, vertical_direction

        # Changing row => changing direction
        next_horizontal_direction = HorizontalDirection.reverse(horizontal_direction)
        next_y = y + vertical_direction.value

        if self._pad_grid.height > next_y >= 0:
            return x, next_y, next_horizontal_direction, vertical_direction

        next_vertical_direction = VerticalDirection.reverse(vertical_direction)
        next_y = y + next_vertical_direction.value

        return x, next_y, next_horizontal_direction, next_vertical_direction
