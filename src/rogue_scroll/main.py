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
import sys

if sys.version_info < (3, 10):
    raise RuntimeError("This requires Python 3.10+")

import secrets  # we will not use the RNG from original rogue.
import math
import argparse
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


# All defaults can be set to other values on the command line.
DEFAULT_N = 1  # Scroll titles to generate
DEFAULT_K = False
DEFAULT_BIG_K = False


class _CombinedArgParseFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter,
):
    pass


parser = argparse.ArgumentParser(
    prog="scroll_gen",
    formatter_class=_CombinedArgParseFormatter,
    description=__doc__,
    epilog="Copyright AgileBits, Inc. 2022; Jeffrey Goldberg 2024–2025",
)
parser.add_argument(
    "-s",
    "--min-syllables",
    type=int,
    default=Scroll.DEFAULT_MIN_S,
    help="minimum syllables per word",
)
parser.add_argument(
    "-S",
    "--max-syllables",
    type=int,
    default=Scroll.DEFAULT_MAX_S,
    help="maximum syllables per word",
)

parser.add_argument(
    "-w",
    "--min-words",
    type=int,
    default=Scroll.DEFAULT_MIN_W,
    help="minimum words per title",
)
parser.add_argument(
    "-W",
    "--max-words",
    type=int,
    default=Scroll.DEFAULT_MAX_W,
    help="maximum words per title",
)
parser.add_argument(
    "-n",
    type=int,
    default=DEFAULT_N,
    help="number of scroll titles to generate",
)
parser.add_argument(
    "-k",
    action="store_true",
    default=DEFAULT_K,
    help="show kind of scroll",
)
parser.add_argument(
    "-K",
    action="store_true",
    default=DEFAULT_BIG_K,
    help="only show kind of scroll",
)
parser.add_argument(
    "--entropy", "-H", help="compute entropy", action="store_true"
)


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


def main() -> None:
    args = parser.parse_args()
    syllables = MinMax(args.min_syllables, args.max_syllables)
    words = MinMax(args.min_words, args.max_words)

    # The functions we call will throw TypeErrors if these
    # conditions aren't met, but we can produce more helpful errors
    # here in main()
    if not is_min_max(syllables):
        raise ValueError(
            f"minimum number of syllables ({syllables.min}) can't be"
            f"greater than maximum ({syllables.max})"
        )

    if not is_min_max(words):
        raise ValueError(
            f"minimum number of words ({words.min}) can't be"
            f"greater than maximum ({words.max})"
        )

    if args.n < 0:
        raise ValueError(f"You owe me {-args.n} scroll titles.")

    for _ in range(args.n):
        kind = ""
        title = ""
        output = ""
        if not args.K:
            title = Scroll.generate_title(syllables, words)
        if args.k or args.K:
            kind = Scroll.choose()
        match args.k, args.K:
            case False, False:
                output = title
            case True, False:
                output = f"{title} [{kind}]"
            case _, True:
                output = kind
        print(output)

    if args.entropy:
        print(Scroll.entropy(syllables, words))


if __name__ == "__main__":
    main()
