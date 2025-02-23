# Generate Rogue scroll titles

[rogue]: https://en.wikipedia.org/wiki/Rogue_(video_game) "Wikipedia: Rogue game"
[rsrc]: https://github.com/Davidslv/rogue/ "GitHub: rogue source"

In the game [rogue], the player comes across scrolls with random titles.
This tool can be used to generate such titles,
but using a cryptographically secure random number generator
instead of [the original RNG (PDF)](https://jpgoldberg.github.io/sec-training/s/rogue-lcg.pdf).

The [source][rsrc] I am using for the syllables used in scroll titles for the 
default numbers of syllables per word and words per title come from the copy of rogue
version 5.4.4 source managed by [David Silva](https://github.com/Davidslv/) at
<https://github.com/Davidslv/rogue/>

This tool also provides a mechanism to pick the kinds of scrolls using the same probability distribution as in [rogue].

## License

Released under [Creative Commons Attribution-Noderivatives version 4.0 license](https://creativecommons.org/licenses/by-nd/4.0/).
Copyright AgileBits, Inc. 2022; Jeffrey Goldberg 2024–2025.
