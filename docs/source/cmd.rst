=========================
The rogue-scroll command
=========================

.. argparse::
    :module: rogue_scroll.__main__
    :func: parser
    :prog: rogue-scroll

Examples
==========


Syllables per word and words per title (``-s``, ``-S``, ``-w``, ``-W``)
------------------------------------------------------------------------

The default will generate a single random scroll title with the parameters for the minimum and maximum number of syllables per word
and the minimum and maximum number of words per title.

.. ::

    The defaults are 

    .. autoattribute:: rogue_scroll.Generator.DEFAULT_MIN_S
        :no-index:

    .. autoattribute:: rogue_scroll.Generator.DEFAULT_MAX_S
        :no-index:

    .. autoattribute:: rogue_scroll.Generator.DEFAULT_MIN_W
        :no-index:

    .. autoattribute:: rogue_scroll.Generator.DEFAULT_MAX_W
        :no-index:

.. code:: console

    $ rogue-scroll
    e it niher rhovwahfri

If we want to at least two syllables per word

.. code:: console

    $ rogue-scroll -s 2
    zebaks sunanash yotsne

If we wanted to ensure that a scroll title is exactly five words

.. code:: console

    $ rogue-scroll -w5 -W5
    ipox ro saip mur erzok

Note that if the minimum is greater than the maximum, ``rogue-scroll`` will use
the minimum as the fixed length

.. code:: console

    $ rogue-scroll -w4 -W1
    itpotpay satfa nelgitesol dalfti

    $ rogue-scroll -S2 -s4
    fubumike klisuvivash ereyutiseh


Number of scroll titles to generate (``-n``)
----------------------------------------------

It is posssible to generate any non-negative number (including zero) of scrolls
using the ``-n`` option.

.. code:: console

    $ rogue-scroll -n3
    sanresun zebnihplu umnep
    sef rososef
    klis reaakssnik

    $ rogue-scroll -n0

Entropy (``-H``)
-------------------

With the ``-H`` flag, the entropy from the generator settings will be printed
after the scroll titles.

.. code:: console

    $ rogue-scroll  -H
    marzokevs ash
    86.43545791624923

Because the entropy is a function of the settings for
number of words and syllables it is only printed once.

.. code:: console

    $ rogue-scroll -n3 -H
    wedkli ulkrog
    erod zumklis tursganood wergdalf
    eshengash wedpo
    86.43545791624923

If you only want to entropy for some particular settings, you can combine this with ``-n0`` to not generate any titles.
Here we see that calculation for five syllables per word and five words per title:

.. code:: console

    $ rogue-scroll -W5 -S5 -n0 -H
    180.04104755060663

.. warning::

    Entropy computation can be higher than true value. See :ref:`prefix` for details.

Kinds of scrolls (``-k``, ``-K``)
----------------------------------

There are 18 kinds of scrolls in rogue_, listed in
:data:`Constants.SCROLL_KINDS`, which turn up with distinct probabilities.
For example when one finds a scroll
there is a 10% chance that it will be a scroll of “identify potion”,
while only a 2% change that it will be a scroll of “protect armor".
|cmd| can assign scroll kinds according to those probabilities.

With the ``-k`` command line flag, the kind of scroll will be listed
with the generated title:

.. code:: console

    $ rogue-scroll -n4 -k
    klis ityot wun [enchant armor]
    xobek ere [aggravate monsters]
    nejturs eepwun [identify ring, wand or staff]
    evs zimfidfri fu [identify ring, wand or staff]


With the ``-K`` option, only the kinds will be listed.
Titles will not be generated.

.. code:: console

    $ rogue-scroll -n4 -K
    identify potion
    identify armor
    enchant weapon
    monster confusion


.. _d_option:

Syllable divider (``-d``, `--syllable-divider`)
--------------------------------------------------

By default there is no separator between syllables
in title words.
That is fine except that it can result in incorrect entropy
computation, as there may be multiple ways a particular title workd could be generated.
See :ref:`prefix` for details.

So for some usages we may want to set a separator character,
such as “``-``”.

.. code:: console

    $ rogue-scroll -d+
    shu+re plu wun+it
