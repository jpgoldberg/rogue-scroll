"""
This file includes extremely expensive and probabilistic sanity checks.
It should not be run as part of any automated thing.
"""

from rogue_scroll import Scroll
import pandas as pd
from scipy import stats


def scroll_historgram(trials: int = 1000) -> dict[str, int]:
    hist = {s: 0 for s in Scroll.SCROLLS.keys()}

    for _ in range(trials):
        s = Scroll.choose()
        hist[s] = hist[s] + 1
    return hist


class DistData:
    def __init__(self, hist: dict[str, int]) -> None:
        prob_total = sum(Scroll.SCROLLS.values())
        trials = sum(hist.values())
        multiplier = trials / prob_total
        expected = {s: p * multiplier for s, p in Scroll.SCROLLS.items()}

        self.data: dict[str, tuple[int, float]] = {
            s: (hist[s], expected[s]) for s in hist
        }

    def as_dataframe(self) -> pd.DataFrame:
        d: dict[str, list[str | float]] = dict()
        d["scroll_type"] = [s for s in self.data.keys()]
        d["count"] = [v[0] for v in self.data.values()]
        d["expected"] = [v[1] for v in self.data.values()]
        df = pd.DataFrame(d)
        return df

    def __str__(self) -> str:
        return str(self.as_dataframe())

    def ks(self) -> tuple[float, float]:
        """Returns (statistic, pvalue) from ks_2samp test.

        The p-values treat the null hypothesis as distributions are identical.
        """
        counts: list[int] = []
        expectations: list[float] = []
        for c, e in self.data.values():
            counts.append(c)
            expectations.append(e)
        res = stats.ks_2samp(
            counts, expectations, alternative="two-sided", method="auto"
        )

        return res.statistic, res.pvalue


def main() -> None:
    hist = scroll_historgram(10_000)
    data = DistData(hist)

    print(data)
    p = 1.0 - data.ks()[1]
    print(f"p-value: {p:.4g}")


if __name__ == "__main__":
    main()
