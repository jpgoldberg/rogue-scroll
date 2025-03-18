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

    def test_min_eq_max(self) -> None:
        trials = 20
        top = 10
        for min in range(1, top):
            g = rs.Generator(
                min_syllables=1, max_syllables=1, min_words=min, max_words=min
            )
            for _ in range(trials):
                s = g.random_title()
                n = s.count(" ") + 1
                assert n == min

    def test_min_gt_max(self) -> None:
        trials = 20
        top = 10
        for min in range(1, top):
            g = rs.Generator(
                min_syllables=1, max_syllables=1, min_words=min, max_words=1
            )
            for _ in range(trials):
                s = g.random_title()
                n = s.count(" ") + 1
                assert n == min


class TestMaxWords:
    def test_max_gt_min(self) -> None:
        trials = 20
        maximax = 10
        for max in range(1, maximax):
            g = rs.Generator(
                min_syllables=1, max_syllables=1, min_words=1, max_words=max
            )
            for _ in range(trials):
                s = g.random_title()
                n = s.count(" ") + 1
                assert n <= max


class TestZeroWords:
    def test_max_eq_zero(self) -> None:
        trials = 20
        g = rs.Generator(
            min_syllables=1, max_syllables=1, min_words=0, max_words=0
        )
        for _ in range(trials):
            s = g.random_title()
            assert s == ""


if __name__ == "__main__":
    sys.exit(pytest.main(args=[__file__]))
