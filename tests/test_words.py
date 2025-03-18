import sys
import pytest

import rogue_scroll as rs


class TestMinWords:
    def test_min_lt_max(self) -> None:
        trials = 20
        max = 10
        for min in range(1, max):
            g = rs.Generator(
                min_syllables=1, max_syllables=1, min_words=min, max_words=max
            )
            for _ in range(trials):
                s = g.random_title()
                n = s.count(" ") + 1
                assert n >= min


if __name__ == "__main__":
    sys.exit(pytest.main(args=[__file__]))
