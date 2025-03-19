=========================
As a password generator?
=========================

The question naturally (well, for some of us) arises whether |project| is suitable for generating secure and practical passwords.
The short answer is yes for security (with the right settings), 
but they are practical only for limited circumstances.

Secure
========

With appropriate settings (see :ref:`prefix`) scroll titles are
*uniformly distributed*,
and they are generated using a
cryptographgically secure random number generator.
Under these assumptions we can compute the entropy of the generator given specific parameters.

With three syllables per word and four words,
a generated title has more than 86 bits of entropy.
For example at the command line,

.. code:: console

    $ rogue-scroll -s3 -S3 -w4 -W4 -d- -H 
    ing-vly-rhov whon-mic-eng vly-bot-bie dalf-u-arze

or though the module

.. testcode::

    from rogue_scroll import Generator

    g = Generator(
            min_words = 4, max_words = 4,
            min_syllables=3, max_syllables=3,
            separator='-',
        )
    new_pwd = g.random_title()
    H = g.entropy()
    if H > 85:
        print(f"Exceedingly strong: H = {H:.2f}")
    else:
        print(f"This shouldn't have happened: H = {H:.2f}")
    
.. testoutput::

    Exceedingly strong: H = 86.40


That sample code also serves as a reminder
that entropy is not a function of the generated password
but is a function of the generator.

Practicality
==============

Generatoed rogue scroll titles

1. are not particularly memorable;
2. do not contain digits, uppercase letters, or symbols;
3. do contain spaces.

That limits their utility vastly,
but there are still some practical uses for them.
Because they are all lower case letters and spaces,
they are relatively easy to type on a mobile keyboard compared to other
things of a similar length.

The sorts of uses listed here assume that you are using a password manager so that you do not have to memorize these.

Insecurity questions
---------------------

Who doesn't want to say that their favorite teacher was “elan klivly labekum nelg”
or that their father's middle name is “vly prokbit iv roglanej”?

Infrequently typed local passwords
-----------------------------------

These can include home wifi passwords that you enter into each device just once. Passwords for disk encryption are typically only used when setting up the device or when the disk needs to be attached to a new device.

I am not claiming that these are better suited then many other password generation schemes, but they are fun. Particularly for those of us who spent way too much time playing rogue_.

