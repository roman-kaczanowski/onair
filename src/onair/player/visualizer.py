import math
import random
import time

# ponytail: decorative levels while playing; upgrade to VLC PCM/FFT for a real spectrum.
BANDS = 32
ROWS = 2


class Meter:
    def __init__(self) -> None:
        self.levels = [0.0] * BANDS

    def tick(self, active: bool) -> list[float]:
        if not active:
            self.levels = [level * 0.55 for level in self.levels]
            return self.levels
        t = time.monotonic()
        for index in range(BANDS):
            wave = abs(math.sin(t * (1.4 + index * 0.11) + index))
            target = 0.15 + 0.85 * wave * (0.35 + 0.65 * random.random())
            self.levels[index] = self.levels[index] * 0.55 + target * 0.45
        return self.levels


def render_histogram(levels: list[float], indent: str = '') -> str:
    rows = [[' ' for _ in levels] for _ in range(ROWS)]
    for column, level in enumerate(levels):
        height = min(ROWS, max(0, round(level * ROWS)))
        for row in range(height):
            rows[ROWS - 1 - row][column] = '#'
    return '\n'.join(indent + ''.join(row) for row in rows)
