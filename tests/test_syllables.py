import sys
import pytest

import rogue_scroll as rs


class TestSyllableIsSyllable:
    def test_single(self) -> None:
        trials = 10
        g = rs.Generator(
            min_syllables=1,
            max_syllables=1,
            min_words=1,
            max_words=1,
        )
        for _ in range(trials):
            s = g.random_title()
            assert s in rs.Constants.SYLLABLES

    def test_lots(self) -> None:
        max_words = 10
        max_syllables = 10
        trials = 5
        g = rs.Generator(
            min_syllables=2,
            max_syllables=max_syllables,
            min_words=1,
            max_words=max_words,
            separator="-",
        )
        for _ in range(trials):
            # Yes, what follows could just use all() and a comprehension
            # but tests are for debugging.
            title = g.random_title()
            for word in title.split(" "):
                syllables = word.split("-")
                for s in syllables:
                    assert s in rs.Constants.SYLLABLES


class TestMinSyllables:
    def test_min_lt_max(self) -> None:
        trials = 20
        max = 10
        for min in range(1, max):
            g = rs.Generator(
                min_syllables=min,
                max_syllables=max,
                min_words=1,
                max_words=1,
                separator="-",
            )
            for _ in range(trials):
                s = g.random_title()
                n = s.count("-") + 1
                assert n >= min

    def test_min_eq_max(self) -> None:
        trials = 20
        top = 10
        for min in range(1, top):
            g = rs.Generator(
                min_syllables=min,
                max_syllables=min,
                min_words=1,
                max_words=1,
                separator="-",
            )
            for _ in range(trials):
                s = g.random_title()
                n = s.count("-") + 1
                assert n == min

    def test_min_gt_max(self) -> None:
        trials = 20
        top = 10
        for min in range(1, top):
            g = rs.Generator(
                min_syllables=min,
                max_syllables=1,
                min_words=1,
                max_words=1,
                separator="-",
            )
            for _ in range(trials):
                s = g.random_title()
                n = s.count("-") + 1
                assert n == min


class TestMaxSyllables:
    def test_max_gt_min(self) -> None:
        trials = 20
        maximax = 10
        for max in range(1, maximax):
            g = rs.Generator(
                min_syllables=1,
                max_syllables=max,
                min_words=1,
                max_words=1,
                separator="-",
            )
            for _ in range(trials):
                s = g.random_title()
                n = s.count("-") + 1
                assert n <= max


class TestZeroSyllables:
    def test_max_eq_zero(self) -> None:
        trials = 20
        g = rs.Generator(
            min_syllables=0, max_syllables=0, min_words=1, max_words=1
        )
        for _ in range(trials):
            s = g.random_title()
            assert s == ""


if __name__ == "__main__":
    sys.exit(pytest.main(args=[__file__]))
