"""Rogue scroll title generator

This script generates random scroll titles in the style of the
game Rogue by Michael Toy, Ken Arnold and Glenn Wichman, originally
developed in the early 1980s.

Scrolls in the game had titles like

    "potrhovbek sunsnefa wunit vlysnebek"

This file can also be imported as a module
"""

# NamedTuple type hints come with python 3.6. TypeGuard with 3.10.
from bisect import bisect
from itertools import accumulate

import secrets  # we will not use the RNG from original rogue.
import math
from typing import NamedTuple, TypeGuard


class MinMax(NamedTuple):
    """Minimum and maximum"""

    min: int
    max: int


def is_min_max(mm: tuple[int, int]) -> TypeGuard[MinMax]:
    if not isinstance(mm, tuple):
        return False
    if len(mm) != 2:
        return False
    if not (isinstance(mm[0], int) and isinstance(mm[1], int)):
        return False
    if mm[1] < mm[0]:
        return False
    return True

def rand_in_range(r: MinMax) -> int:
    """Return a uniformly chosen random in [bottom, top] inclusive."""

    diff = r.max - r.min
    if diff == 0:
        return r.min

    return secrets.randbelow(diff + 1) + r.min


def count_possibilities(n: int, min: int, max: int) -> int:
    """:math:`\\sum_{x=min}^{max} n^x`

    :raises ValueError: if max > min.
    :raise ValueError: if n < 1.
    """

    if not is_min_max((min, max)):
        raise ValueError("Minimum can't be greater than maximum.")

    if n < 1:
        raise ValueError("n must be positive")

    total = 0
    for length in range(min, max + 1):
        total += n**length
    return total


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

    # None is used as a sentinel for not yet computed
    _breakpoints: list[int] | None = None
    _max_prob: int | None = None

    # Defaults taken from hardcoded values in rogue source.
    DEFAULT_MIN_S = 1  # Minimum syllables per word
    DEFAULT_MAX_S = 3  # Maximum syllables per word
    DEFAULT_MIN_W = 2  # Minimum words per title
    DEFAULT_MAX_W = 4  # Maximum words per title

    @classmethod
    def cumulative(cls) -> list[int]:
        if cls._breakpoints is None:
            c = list(accumulate(cls.SCROLLS.values()))
            base = c.pop(0)
            cls._breakpoints = list(map(lambda x: x - base, c))
            cls._max_prob = sum(cls.SCROLLS.values())
        return cls._breakpoints

    @classmethod
    def choose(cls) -> str:
        """Randomly picks a scroll using weighted probabilities."""

        breakpoints: list[int] = cls.cumulative()
        scroll_types: list[str] = list(cls.SCROLLS.keys())
        assert cls._max_prob is not None  # for type narrowing
        assert len(breakpoints) == len(scroll_types) - 1

        score = secrets.randbelow(cls._max_prob) + 1
        i = bisect(breakpoints, score)
        return scroll_types[i]

    @classmethod
    def generate_title(
        cls, syllables_per_word: MinMax, words_per_title: MinMax
    ) -> str:
        """Generate a scroll title

        Parameters
        ----------
        syllables_per_word: tuple[int, int]
            The [minimum, maximum] number of syllables to construct each word from
        words_per_title: tuple[int, int]
            The [minimum, maximum] number of words in the scroll title

        Returns
        -------
        str
            A scroll title
        """

        n_words = rand_in_range(words_per_title)

        words: list[str] = []
        for w in range(n_words):
            n_syllables = rand_in_range(syllables_per_word)
            word = ""
            for s in range(n_syllables):
                syl = cls.SYLLABLES[secrets.randbelow(len(cls.SYLLABLES))]
                word += syl

            words.append(word)
        return " ".join(words)

    @staticmethod
    def _count_possibilities(n: int, min: int, max: int) -> int:
        """:math:`\\sum_{x=min}^{max} n^x`

        :raises ValueError: if max > min.
        :raise ValueError: if n < 1.
        """

        if not is_min_max((min, max)):
            raise ValueError("Minimum can't be greater than maximum.")

        if n < 1:
            raise ValueError("n must be positive")

        total = 0
        for length in range(min, max + 1):
            total += n**length
        return total

    @classmethod
    def entropy(
        cls, syllables_per_word: MinMax, words_per_title: MinMax
    ) -> float:
        """Entropy in bits given numbers of syllables per word, words per title."""

        # This code assumes that the maximum number of syllables per words
        # and words per syllables will remain small.
        # With larger numbers there would be more efficient ways to do this.
        words = count_possibilities(
            len(cls.SYLLABLES), syllables_per_word.min, syllables_per_word.max
        )
        titles = count_possibilities(
            words, words_per_title.min, words_per_title.max
        )

        return math.log2(titles)
