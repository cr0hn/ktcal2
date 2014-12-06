# -*- coding: utf-8 -*-

"""
This file contains data structures
"""

__license__ = '''Copyright (c) cr0hn - cr0hn<-at->cr0hn.com (@ggdaniel) All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of cr0hn nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.'''
__author__ = 'cr0hn - cr0hn<-at->cr0hn.com (@ggdaniel)'

from itertools import tee
from collections import namedtuple


# --------------------------------------------------------------------------
class PasswordConfig:
    """Structure to store password configuration"""

    # ----------------------------------------------------------------------
    def __init__(self, **kwargs):
        """
        :param low_chars: Select low characters. From a-z.
        :type low_chars: bool

        :param upper_chars: Select low characters. From A-Z.
        :type upper_chars: bool

        :param numbers: Select numbers 0-9.
        :type numbers: bool

        :param special: Select special chars: -_.;+&%
        :type special: bool

        :param special_long: Select special chars: '¿?=)(/$·"!+{}><
        :type special_long: bool

        :param max_len: Set maximum password len. Default 4.
        :type max_len: int
        
        :param min_len: Set minimum password len: 1.
        :type min_len: int
        
        :raises: TypeError
        """
        self.low_chars = kwargs.get("low_chars", False)
        self.upper_chars = kwargs.get("upper_chars", False)
        self.numbers = kwargs.get("numbers", True)
        self.special = kwargs.get("special", False)
        self.special_long = kwargs.get("special_long", False)
        self.max_len = kwargs.get("max_len", 0)
        self.min_len = kwargs.get("min_len", 4)

        if not isinstance(self.max_len, int):
            raise TypeError("Expected int, got '%s' instead" % type(self.max_len))
        if not isinstance(self.min_len, int):
            raise TypeError("Expected int, got '%s' instead" % type(self.min_len))


# --------------------------------------------------------------------------
class FoundCredential:
    """Structure to store password credentials."""

    # ----------------------------------------------------------------------
    def __init__(self, **kwargs):
        """
        :param user: Found user credential.
        :type user: str

        :param password: Found password credential.
        :type password: str
        """
        self.user = kwargs.get("user")
        self.password = kwargs.get("password")


# --------------------------------------------------------------------------
class GlobalParameters:
    """Global execution parameters"""

    # ----------------------------------------------------------------------
    def __init__(self, **kwargs):
        """
        :param target: destination target 
        :type target: str
        
        :param verbosity: verbosity level. From 0 to 2 
        :type verbosity: int
        
        :param concurrency: maximum number of concurrent connections.
        :type concurrency: int

        :param delay: delay time between each password test.
        :type delay: float

        :param port: remote SSH port.
        :type port: int

        :param username_list: iterator with users: ["user1", "user2"]
        :type username_list: generator(str)

        :param password_config: Password configuration
        :type password_config: :class:`lib.data.PasswordConfig`

        :param password_list: iterator with passwords: ["password1", "password2"]
        :type password_list: generator(str)
        
        :param display_function: function used to display debug information. 
        :type display_function: function
        
        :raises: TypeError, ValueError
        """
        # Main
        self.target = kwargs.get("target")
        self.verbosity = kwargs.get("verbosity", 0)

        # Network
        self.concurrency = kwargs.get("concurrency", 20)
        self.delay = kwargs.get("delay", 0)
        self.port = kwargs.get("port", 22)

        # Credentials
        self.user_list = kwargs.get("username_list")

        # Password info
        self.password_config = kwargs.get("password_config")
        self.__password_list = None
        self.__password_list_backup = kwargs.get("password_list")
        self.__password_from_file = True if self.__password_list_backup is not None else False
        self.__rebuild_passwords()

        # Callbacks
        self.display_function = kwargs.get("display_function", None)

        if self.user_list is not None:
            if self.user_list.__class__.__name__ != "generator":
                raise TypeError("Expected generator, got '%s' instead" % type(self.user_list))
        else:
            raise TypeError("Expected generator, got '%s' instead" % type(self.user_list))

    # ----------------------------------------------------------------------
    def __generate_passwords(self, password_config):
        """
        Creates a generator with all combinations of passwords using configuration
        object.

        :param password_config: Password configuration
        :type password_config: PasswordConfig

        :return: generator with passwords
        :rtype: generator(str)

        :raises: ValueError
        """
        from itertools import product

        if not isinstance(password_config, PasswordConfig):
            raise TypeError("Expected PasswordConfig, got '%s' instead" % type(password_config))

        min_len = password_config.min_len
        max_len = password_config.max_len + 1
        if min_len < 1:
            raise ValueError("Password len must be greater than 0")
        if max_len < 1:
            raise ValueError("Password len must be greater than 0")
        if min_len > max_len:
            raise ValueError("Password min len must be greater than maximum len")

        key_space = ""

        if password_config.low_chars:
            key_space += "abcdefghijlmnopqrstuwxyz"
        if password_config.upper_chars:
            key_space += "ABCDEFGHIJKLMNOPQRSTUVWZYZ"
        if password_config.numbers:
            key_space += "0123456789"
        if password_config.special:
            key_space += "-_.;+&%"
        if password_config.special_long:
            key_space += "'¿?=)(/$·\"!+{}><"

        if key_space == "":
            raise ValueError("Key space is empty. Configure password properlty")

        for x in range(min_len, max_len):
            for word in product(key_space, repeat=x):
                yield ''.join(word)

    # ----------------------------------------------------------------------
    def __rebuild_passwords(self):
        """Rebuild generator list"""
        if self.__password_from_file is False:
            if self.password_config is None:
                raise ValueError("Password config required")

            self.__password_list = self.__generate_passwords(self.password_config)
        else:
            self.__password_list, self.__password_list_backup = tee(self.__password_list_backup)

    # ----------------------------------------------------------------------
    @property
    def password_list(self):
        """
        :return: Generator with passwords
        :rtype: generator(str)
        """
        regenerate = True

        for x in self.__password_list:
            regenerate = False
            yield x

        if regenerate:
            self.__rebuild_passwords()

        yield from self.__password_list