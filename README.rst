What's this project?
====================

This project aims to perform a library/tool make a SSH brute force password attack that you can use **as a library as a command line tool**.

The goal of ktcal2 is that it uses new **non-blocking I/O AsyncIO framework**, included **Python 3.4**. 

Some links:

 - **Documentation:** `<http://ktcal2.readthedocs.org>`_ (currently not working).
 - AsyncSSH: This project use `AsyncSSH <https://github.com/ronf/asyncssh>`_ library internally.



Licence
=======

This project is **BSD**... Copy it! And, if you remember, please mention me in credits :)

How to install
==============

PIP
---

.. code-block:: bash

    sudo python3.4 -m pip install PyCrypto
    sudo python3.4 -m pip install ktcal2
    kt-cal2 -h

Manually
--------

.. code-block:: bash

    sudo python3.4 -m pip install PyCrypto
    git clone https://github.com/cr0hn/ktcal2.git ktcal2
    cd ktcal2
    sudo python3.4 -m pip -r requirements.txt install
    python3.4 kt-cal2.py -h

How use it?
===========

You can use this project in command line tool or as a library, in your Python projects.

As a tool
---------

You can test SSH passwords, using a wordlist or brute forcer password generation.
 
Using wordlist
______________

Basic usage:

.. code-block:: bash

    python3.4 ktcal2.py --password-wordlist my_password_list.txt -u root 127.0.0.1

Using user name wordlist:

.. code-block:: bash

    python3.4 ktcal2.py --password-wordlist my_password_list.txt --user-wordlist user_names.txt 127.0.0.1
 
Using password wordlist brute force
___________________________________

ktcal2 can generates all combinations of wordlist based in rules.

If we want to generate all combinations, with 4 word length **(--max-length 4)** using only **numbers (-N), 0000-9999**:  

.. code-block:: bash

    python3.4 ktcal2.py -u root --max-length 4 -N 127.0.0.1

All combinations. 2 max and minimum length, only numbers 00-99:

.. code-block:: bash

    python3.4 ktcal2.py -u root -N --max-length 2 --min-length 2 127.0.0.1

All combinations. 2 max and minimum length. Using numbers, low and upper letters (00..aa..AA):

.. code-block:: bash

    python3.4 ktcal2.py -u root -N -c -C --max-length 2 --min-length 2 127.0.0.1

As a library
------------

.. code-block:: python

    from ktcal2.api import run
    from ktcal2.lib.data import GlobalParameters, PasswordConfig
        
    def custom_display(message):
        """Displays debug info in a custom way"""
        print("----->>> %s <<<-----" % message)
        
        
    if __name__ == "__main__":
        # Configure password generator, for brute forcer mode.
        password_config = PasswordConfig(low_chars=True,
                                     numbers=True,
                                     special=True,
                                     min_len=4,
                                     max_len=5)

        config = GlobalParameters(target=dst,
                                  verbosity=2,

                                  # If we wan to display info
                                  display_function=custom_display,

                                  # Net options
                                  concurrency=20,

                                  # Credentials
                                  username_list=("root" for x in range(1)),
                                  password_config=password_config)
        
        run(config)
        
