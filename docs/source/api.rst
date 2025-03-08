API
====

.. automodule:: rogue_scroll
    :members:


Examples
--------

Note that because output is random, it is a bit tricky to contrive doctests.

.. testcode::

    from rogue_scroll import Generator, Scroll, Constants

Entropy computations are not random are a function of the parameters used to create a Generator

.. testcode::

    g = Generator()  # default values
    H = g.entropy()
    print(f"{H:.2f}")

.. testoutput::

    86.44

An example in which we generate between 4 and 6 words, inclusive

.. testcode::

    g = Generator(min_words = 4, max_words = 6)
    for _ in range(5):
        title = g.random_title()
        word_count = len(title.split())
        assert word_count >= 4 and word_count <= 6
        print(f'"{title}" has {word_count} words')

.. testoutput::
    :hide:

    "..." has ... words
    "..." has ... words
    "..." has ... words
    "..." has ... words
    "..." has ... words

That might produce an output such as

.. code-block:: text

    "ulk rhovmonbie uni orgrhov con ha" has 6 words
    "potfucomp zeburta zok neriteklis" has 4 words
    "bjorapp alaha bek biebekso fuuniu" has 5 words
    "alapo ninan hyditsne ple" has 4 words
    "erkbublu rhov alala arzeshunelg" has 4 words

We also create scrolls of various kinds using the probability weights from the orginal game.

.. testcode::

    for _ in range(5):
        k = Generator.random_kind()
        assert k in Constants.SCROLL_KINDS
        print(f'a scroll of {k}')

.. testoutput::
    :hide:

    a scroll of ...
    a scroll of ...
    a scroll of ...
    a scroll of ...
    a scroll of ...

That would produce an output that looks something like, 

.. code-block:: text

    a scroll of hold monster
    a scroll of identify ring, wand or staff
    a scroll of identify ring, wand or staff
    a scroll of scare monster
    a scroll of enchant armor

One could check that scroll kinds are picked with a probability corresponding
to :data:`~rogue_scroll.Constants.SCROLL_PROBS` by building on something like,

.. testcode::

    hist = {s: 0 for s in Constants.SCROLL_PROBS.keys()}

    trials = 1000
    for _ in range(trials):
        s = Generator.random_kind()
        hist[s] = hist[s] + 1
    
    # we will just look for a few

    row_format = "{:<20} {:>5} {:>10}"
    print(row_format.format("Kind", "Count", "Expected"))
    for k in ['protect armor', 'monster confusion',  'identify potion']:
        expected = round(Constants.SCROLL_PROBS[k] * trials / 100)
        count = hist[k]
        print(row_format.format(k, count, expected))


.. testoutput::
    :hide:

    Kind                 Count   Expected
    ...
    ...
    ...

That would yield results with values something like this,

.. code-block:: text

    Kind                 Count   Expected
    protect armor           19         20
    monster confusion       69         70
    identify potion         95        100

When that example is fleshed out with more useful reporting and run with 10000 trials we get a result like

.. figure:: /images/kind_distribution.png
    :align: center
    :alt: Bar chart showing actual and expected counts of scroll kinds

    Reusts from one run with picking 10,000 scroll kinds. 
    Kolmorogov-Smirnov test statistic is 0.17.