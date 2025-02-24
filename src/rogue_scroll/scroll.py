"""Rogue scroll title generator

This script generates random scroll titles in the style of the
game Rogue by Michael Toy, Ken Arnold and Glenn Wichman, originally
developed in the early 1980s.

Scrolls in the game had titles like

    "potrhovbek sunsnefa wunit vlysnebek"

This file can also be imported as a module
"""

from bisect import bisect
from itertools import accumulate
from typing import NamedTuple

import secrets  # we will not use the RNG from original rogue.
import math


class _PreComputed(NamedTuple):
    scroll_types: list[str]
    cum_weights: list[int]
    hi: int
    total: int


class Scroll:
    """Rogue scroll information."""

    # syllables from https://github.com/Davidslv/rogue/blob/master/init.c#L114
    # spell-checker: disable
    SYLLABLES: list[str] = [
        "a", "ab", "ag", "aks", "ala", "an", "app", "arg", "arze", "ash", "bek",
        "bie", "bit", "bjor", "blu", "bot", "bu", "byt", "comp", "con", "cos",
        "cre", "dalf", "dan", "den", "do", "e", "eep", "el", "eng", "er", "ere",
        "erk", "esh", "evs", "fa", "fid", "fri", "fu", "gan", "gar", "glen", "gop",
        "gre", "ha", "hyd", "i", "ing", "ip", "ish", "it", "ite", "iv", "jo",
        "kho", "kli", "klis", "la", "lech", "mar", "me", "mi", "mic", "mik",
        "mon", "mung", "mur", "nej", "nelg", "nep", "ner", "nes", "nes", "nih",
        "nin", "o", "od", "ood", "org", "orn", "ox", "oxy", "pay", "ple", "plu",
        "po", "pot", "prok", "re", "rea", "rhov", "ri", "ro", "rog", "rok",
        "rol", "sa", "san", "sat",  "sef", "seh", "shu", "ski", "sna", "sne",
        "snik", "sno", "so", "sol", "sri", "sta", "sun", "ta", "tab", "tem",
        "ther", "ti", "tox", "trol", "tue", "turs", "u", "ulk", "um", "un", "uni",
        "ur", "val", "viv", "vly", "vom", "wah", "wed", "werg", "wex", "whon",
        "wun", "xo", "y", "yot", "yu", "zant", "zeb", "zim", "zok", "zon", "zum",
    ]  # fmt: skip
    # spell-checker: enable
    """Syllables taken from rogue source."""

    N_SYLLABLES = len(SYLLABLES)
    """Number of distinct syllables."""

    # name and probability fields from scr_info in
    #  https://github.com/Davidslv/rogue/blob/master/extern.c
    SCROLLS: dict[str, int] = {
        "monster confusion": 7,
        "magic mapping": 4,
        "hold monster": 2,
        "sleep": 3,
        "enchant armor": 7,
        "identify potion": 10,
        "identify scroll": 10,
        "identify weapon": 6,
        "identify armor": 7,
        "identify ring, wand or staff": 10,
        "scare monster": 3,
        "food detection": 2,
        "teleportation": 5,
        "enchant weapon": 8,
        "create monster": 4,
        "remove curse": 7,
        "aggravate monsters": 3,
        "protect armor": 2,
    }
    """Scrolls and "probabilities" taken rogue source.

    Probabilities are chance out of 100.
    """

    N_SCROLLS = len(SCROLLS)
    """Number of different scrolls"""

    # None is used as a sentinel for not yet computed
    _precomp: _PreComputed | None = None

    # Defaults taken from hardcoded values in rogue source.
    DEFAULT_MIN_S = 1  # Minimum syllables per word
    DEFAULT_MAX_S = 3  # Maximum syllables per word
    DEFAULT_MIN_W = 2  # Minimum words per title
    DEFAULT_MAX_W = 4  # Maximum words per title

    def __init__(
        self,
        min_syllables: int = DEFAULT_MIN_S,
        max_syllables: int = DEFAULT_MAX_S,
        min_words: int = DEFAULT_MIN_W,
        max_words: int = DEFAULT_MAX_W,
    ) -> None:
        self._s_max = max(min_syllables, max_syllables)
        self._s_min = min_syllables
        self._w_max = max(min_words, max_words)
        self._w_min = min_words

        # Inclusive differences
        self._s_diff = (self._s_max - self._s_min) + 1
        self._w_diff = (self._w_max - self._w_min) + 1

        self._entropy: float | None = None

    @classmethod
    def _precompute_choose(cls) -> _PreComputed:
        """Precomputes things that will be used in every call to choose()"""
        if cls._precomp is None:
            scroll_types = list(cls.SCROLLS.keys())
            weights = cls.SCROLLS.values()
            cum_weights = list(accumulate(weights))
            total = cum_weights[-1]
            hi = cls.N_SCROLLS - 1

            cls._precomp = _PreComputed(
                scroll_types=scroll_types,
                cum_weights=cum_weights,
                total=total,
                hi=hi,
            )
        return cls._precomp

    @classmethod
    def choose(cls) -> str:
        """Randomly picks a scroll using weighted probabilities."""

        # largely lifted from
        # https://github.com/python/cpython/blob/bbfae4a912f021be44f270a63565a0bc2d156e9f/Lib/random.py#L458
        # But we are dealing with integers only,
        # and I am using lots of intermediate variables

        pc = cls._precompute_choose()

        r = secrets.randbelow(pc.total)
        position = bisect(pc.cum_weights, r, 0, pc.hi)
        return pc.scroll_types[position]

    def random_title(self) -> str:
        """Generate random scroll title."""

        n_words: int
        if self._w_diff == 1:
            n_words = self._w_min
        else:
            n_words = secrets.randbelow(self._w_diff) + self._w_min

        # If the number of syllables will be fixed as a single number,
        # we only compute that once.
        fixed_n_syl = False
        n_syllables = -1  # I wish PEP 661 was adopted
        if self._s_diff == 1:
            n_syllables = self._s_min
            fixed_n_syl = True
        else:
            # We will need to compute n_syllables for each word in the
            # loop below.
            fixed_n_syl = False

        words: list[str] = []
        for w in range(n_words):
            if not fixed_n_syl:
                n_syllables = secrets.randbelow(self._s_diff) + self._s_min
            word = ""
            for s in range(n_syllables):
                syl = self.SYLLABLES[secrets.randbelow(self.N_SYLLABLES)]
                word += syl

            words.append(word)
        return " ".join(words)

    @staticmethod
    def count_possibilities(n: int, min: int, max: int) -> int:
        """:math:`\\sum_{x=min}^{max} n^x`

        Note that this can return 0. Keep that in mind if you wish to
        take the logarithm of the result.

        :raises ValueError: if min > max.
        :raise ValueError: if n < 1.
        """

        if max < min:
            raise ValueError("Minimum can't be greater than maximum.")

        if n < 1:
            raise ValueError("n must be positive")

        total = 0
        for length in range(min, max + 1):
            total += n**length
        return total

    def entropy(self) -> float:
        """Entropy in bits.

        :raises ValueError: if no titles would be possible
        """

        if self._entropy is not None:
            return self._entropy

        # This code assumes that the maximum number of syllables per words
        # and words per syllables will remain small.
        # With larger numbers there would be more efficient ways to do this.
        words = self.count_possibilities(
            self.N_SYLLABLES, self._s_min, self._s_max
        )
        titles = self.count_possibilities(words, self._w_min, self._w_max)

        try:
            H = math.log2(titles)
        except ValueError:
            raise

        self._entropy = H
        return self._entropy
