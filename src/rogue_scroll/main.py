"""Rogue scroll title generator

This script generates random scroll titles in the style of the
game Rogue by Michael Toy, Ken Arnold and Glenn Wichman, originally
developed in the early 1980s.

Scrolls in the game had titles like

    "potrhovbek sunsnefa wunit vlysnebek"

This file can also be imported as a module
"""

import sys

if sys.version_info < (3, 10):
    raise RuntimeError("This requires Python 3.10+")

import argparse
from rogue_scroll import Scroll
from rogue_scroll.__about__ import __version__, __copyright__


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
    prog="rogue_scroll",
    formatter_class=_CombinedArgParseFormatter,
    description=__doc__,
    epilog=f"Version {__version__}. {__copyright__}",
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


def main() -> None:
    args = parser.parse_args()

    if args.n < 0:
        raise ValueError(f"You owe me {-args.n} scroll titles.")

    generator = Scroll(
        args.min_syllables, args.max_syllables, args.min_words, args.max_words
    )

    for _ in range(args.n):
        kind = ""
        title = ""
        output = ""
        if not args.K:
            title = generator.random_title()
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
        print(generator.entropy())


if __name__ == "__main__":
    main()
