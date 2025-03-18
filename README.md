# Generate Rogue scroll titles

![Tests status](https://github.com/jpgoldberg/rogue-scroll/actions/workflows/pytest.yml/badge.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://docs.astral.sh/ruff/)
![Linting status](https://github.com/jpgoldberg/rogue-scroll/actions/workflows/lint.yml/badge.svg)
![Type check status](https://github.com/jpgoldberg/rogue-scroll/actions/workflows/types.yml/badge.svg)
[![Documentation](https://github.com/jpgoldberg/rogue-scroll/actions/workflows/docs.yml/badge.svg)][docs]
[![License: "CC-BY-ND-4.0](https://licensebuttons.net/l/by-nd/4.0/80x15.png)](https://creativecommons.org/licenses/by-nd/4.0/)

[rogue]: https://en.wikipedia.org/wiki/Rogue_(video_game) "Wikipedia: Rogue game"
[rsrc]: https://github.com/Davidslv/rogue/ "GitHub: rogue source"
[docs]: https://jpgoldberg.github.io/rogue-scroll/ "rogue-scroll documentation"

See the [documentation][docs] for more detail.

In the game [rogue], the player comes across scrolls with random titles.
This tool can be used to generate such titles,
but using a cryptographically secure random number generator
instead of
[the original RNG](https://jpgoldberg.github.io/sec-training/s/rogue-lcg.html).

The [source][rsrc] I am using for the syllables used in scroll titles for the
default numbers of syllables per word and words per title come from the copy of rogue
version 5.4.4 source managed by [David Silva](https://github.com/Davidslv/) at
<https://github.com/Davidslv/rogue/>

This tool also provides a mechanism to pick the kinds of scrolls using the same probability distribution as in [rogue].

## License

Released under [Creative Commons Attribution-Noderivatives version 4.0 license](https://creativecommons.org/licenses/by-nd/4.0/).
Copyright AgileBits, Inc. 2022; Jeffrey Goldberg 2024–2025.
