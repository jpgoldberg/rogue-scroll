API
====

.. automodule:: rogue_scroll
    :members:


Examples
--------

Note that because output is random, it is a bit tricky to contrive doctests.

.. testcode::

    from rogue_scroll import Generator, Scroll

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


