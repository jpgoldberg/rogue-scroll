"""
This file includes extremely expensive and probabilistic sanity checks.
It should not be run as part of any automated thing.
"""

from rogue_scroll import Scroll
import seaborn as sns
import pandas as pd


def scroll_historgram(trials: int = 1000) -> dict[str, int]:
    hist = {s: 0 for s in Scroll.SCROLLS.keys()}

    for _ in range(trials):
        s = Scroll.choose()
        hist[s] = hist[s] + 1
    return hist


def data_prep(hist: dict[str, int]) -> pd.DataFrame:
    prob_total = sum(Scroll.SCROLLS.values())
    trials = sum(hist.values())
    multiplier = trials / prob_total
    expected = {s: p * multiplier for s, p in Scroll.SCROLLS.items()}

    d: dict[str, list[float]] = {s: [hist[s], expected[s]] for s in hist}
    df = pd.DataFrame.from_dict(
        data=d, orient="index", columns=["actual", "expected"]
    )
    return df


def main() -> None:
    hist = scroll_historgram(10_000)
    df = data_prep(hist)

    print(df)


if __name__ == "__main__":
    main()
