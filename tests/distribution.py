"""
This file includes extremely expensive and probabilistic sanity checks.
It should not be run as part of any automated thing.
"""

from rogue_scroll import Generator, Constants
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


SCROLL_PROBS = Constants.SCROLL_PROBS


def scroll_historgram(trials: int = 1000) -> dict[str, int]:
    hist = {s: 0 for s in SCROLL_PROBS.keys()}

    for _ in range(trials):
        s = Generator.random_kind()
        hist[s] = hist[s] + 1
    return hist


class DistData:
    def __init__(self, hist: dict[str, int]) -> None:
        prob_total = sum(SCROLL_PROBS.values())
        trials = sum(hist.values())
        multiplier = trials / prob_total
        expected = {s: p * multiplier for s, p in SCROLL_PROBS.items()}

        self.data: dict[str, tuple[int, float]] = {
            s: (hist[s], expected[s]) for s in hist
        }

        self._df_wide: pd.DataFrame | None = None
        self._df_long: pd.DataFrame | None = None

    @property
    def df_wide(self) -> pd.DataFrame:
        if self._df_wide is not None:
            return self._df_wide
        d: dict[str, list[str | float]] = dict()
        d["scroll_type"] = [s for s in self.data.keys()]
        d["count"] = [v[0] for v in self.data.values()]
        d["expected"] = [v[1] for v in self.data.values()]
        self._df_wide = pd.DataFrame(d)
        return self._df_wide

    @property
    def df_long(self) -> pd.DataFrame:
        if self._df_long is not None:
            return self._df_long
        d = self.df_wide
        self._df_long = pd.melt(frame=d, id_vars=["scroll_type"])
        return self._df_long

    def __str__(self) -> str:
        return str(self.df_wide)

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

    def plot(self) -> sns.FacetGrid:
        g = sns.catplot(
            data=self.df_long,
            kind="bar",
            y="scroll_type",
            x="value",
            hue="variable",
        )
        g.despine(left=True)
        g.set_axis_labels("Count", "")
        assert g.legend is not None
        g.legend.set_title("")

        return g


def main() -> None:
    hist = scroll_historgram(10_000)
    data = DistData(hist)

    print(data)
    ks_stat, inv_p = data.ks()
    p = 1.0 - inv_p
    print(f"KS-stat: {ks_stat:.2}; p-value: {p:.4g}")

    data.plot()
    plt.show()


if __name__ == "__main__":
    main()
