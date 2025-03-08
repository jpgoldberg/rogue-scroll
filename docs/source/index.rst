.. rogue-scroll documentation master file, created by
   sphinx-quickstart on Thu Feb 27 14:29:31 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Generate Rogue scroll titles with rogue-scroll
==============================================


In the game rogue_, the player comes across scrolls with random titles.
This tool can be used to generate such titles,
but using a cryptographically secure random number generator
instead of `the original RNG <https://jpgoldberg.github.io/sec-training/s/rogue-lcg.html>`_.

.. figure:: /images/rogue-now-have-a-scrool.png
   :alt: rogue screenshot: You now have a scroll called 'lavlyesh wexzimnej robytox'
   :align: center

   Upon picking up a scroll of some unknown type, user is told the title of
   of this type of scroll that will be used throughout this instance of the game


The `rogue source <https://github.com/Davidslv/rogue/>`_ I am using for the syllables used in scroll titles for the
default numbers of syllables per word and words per title come from
the copy of rogue version 5.4.4 source managed
by `David Silva <https://gith ub.com/Davidslv/>`_
at `<https://github.com/Davidslv/rogue/>`_

This tool also provides a mechanism to pick the kinds of scrolls using the same probability distribution as in rogue_.

License
--------

Released under `Creative Commons Attribution-Noderivatives version 4.0 license <https://creativecommons.org/licenses/by-nd/4.0/>`_.
Copyright AgileBits, Inc. 2022; Jeffrey Goldberg 2024–2025.



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   cmd
   api

