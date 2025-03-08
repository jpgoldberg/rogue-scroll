=========================
The rogue-scroll command
=========================

.. argparse::
    :module: rogue_scroll.__main__
    :func: parser
    :prog: rogue-scroll

Examples
==========


Syllables per word and words per title
---------------------------------------

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



