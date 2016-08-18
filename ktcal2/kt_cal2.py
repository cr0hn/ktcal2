#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

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


# ----------------------------------------------------------------------
def get_user_list(username, user_wordlist):
    """
    This functions detects if user was passed only one name as parameter or a wordlist path.
    
    Not simultaneous setter are allowed.
    
    :param username: username word 
    :type username: str
    
    :param user_wordlist: path to wordlist 
    :type user_wordlist: str
    
    :return: iterator with user list to test
    :rtype: generator

    :raises: ValueError, IOError
    """
    if username is not None and user_wordlist is not None:
        raise ValueError("Username and user wordlist are not allowed. Select only one.")
    
    if username is None and user_wordlist is None:
        raise ValueError("Username or user wordlist must be specified.")
    
    if username is not None:
        yield username
    else:
        with open(user_wordlist, "rU") as f:
            for word in f:
                if word.startswith("#"):
                    continue
                if word.endswith("\n"):
                    word = word[:-1]
                
                yield word


# ----------------------------------------------------------------------
def get_password_list(password_file):
    """
    Get password list as generator

    :param password_file: path to wordlist
    :type password_file: str

    :return: iterator with user list to test
    :rtype: generator

    :raises: IOError
    """
    if password_file is not None:
        with open(password_file, "rU") as f:
            for word in f:
                if word.startswith("#"):
                    continue
                if word.endswith("\n"):
                    word = word[:-1]
                
                yield word


# ----------------------------------------------------------------------
def main():
    """
    Main function
    """
    import sys
    
    from .api import GlobalParameters, PasswordConfig, run
    
    if sys.version_info <= (3, 4, 0):
        print("\n[!] You need a Python version greater than 3.4\n")
        exit(1)
    
    parser = argparse.ArgumentParser(description='ktcal2 - SSH brute forcer')
    parser.add_argument('target', metavar='TARGET', nargs='+', help='an integer for the accumulator')
    
    # Network options
    group = parser.add_argument_group('Network options')
    group.add_argument('-t', '--max-concurrency', dest='concurrency', default=4, type=int,
                       help='maximum concurrent connections to the target')
    group.add_argument('--delay', dest='delay', default=0.0, type=float,
                       help='delay timeout between each connection')
    group.add_argument('-p', '--port', dest='port', default=22, type=int,
                       help='remote SSH port. Default 22.')
    group.add_argument('-v', dest='verbosity', default=0, action="count",
                       help='verbosity level: -v, -vv, -vvv.')
    
    # Credentials options
    group2 = parser.add_argument_group('Credentials options')
    group2.add_argument('-u', '--username', dest='username', default="root",
                        help='username to test. Default "root"')
    group2.add_argument('--user-wordlist', dest='user_wordlist', default=None,
                        help='wordlist file with users')
    group2.add_argument('--password-wordlist', dest='password_wordlist', default=None,
                        help='wordlist file with passwords. One per line. Brute force if empty.')
    
    # Password types
    group3 = parser.add_argument_group('Password generation for brute force mode')
    group3.add_argument('--max-length', dest='password_max_len', default=5, type=int,
                        help='maximum password len')
    group3.add_argument('--min-length', dest='password_min_len', default=1, type=int,
                        help='minimum password len')
    group3.add_argument('-c', dest='add_low_chars', action="store_true", default=True,
                        help='use lower case chars in password')
    group3.add_argument('-C', dest='add_upper_chars', action="store_true", default=False,
                        help='use upper case chars in password')
    group3.add_argument('-N', dest='add_numbers', action="store_true", default=False,
                        help='user numbers in password')
    group3.add_argument('-s', dest='add_special_basic', action="store_true", default=False,
                        help='use symbols -_.;+&%% in password')
    group3.add_argument('-S', dest='add_special_advanced', action="store_true", default=False,
                        help='use symbols \'¿?=)(/$·"!+{}>< in password')
    
    # Parse command line
    args = parser.parse_args()
    
    # Load user wordlist
    try:
        user_list = get_user_list(args.username, args.user_wordlist)
    except (ValueError, IOError) as e:
        print("[!] Error: ", e)
        exit(1)
    
    # Load password wordlist
    try:
        if args.password_wordlist is not None:
            password_list = get_password_list(args.password_wordlist)
            password_config = None
        else:
            password_list = None
            password_config = PasswordConfig(low_chars=args.add_low_chars,
                                             upper_chars=args.add_upper_chars,
                                             numbers=args.add_numbers,
                                             special=args.add_special_basic,
                                             special_long=args.add_special_advanced,
                                             max_len=args.password_max_len,
                                             min_len=args.password_min_len)
    except (IOError, ValueError) as e:
        print("[!] Error: ", e)
        exit(1)
    
    f = sys.stderr
    
    # Set global config
    try:
        config = GlobalParameters(target=args.target[0],
                                  verbosity=args.verbosity,
                                  # Only for command line
                                  display_function=f.write,
        
                                  # Net options
                                  concurrency=args.concurrency,
                                  delay=args.delay,
                                  port=args.port,
        
                                  # Credentials
                                  username_list=user_list,
                                  password_list=password_list,
                                  password_config=password_config
                                  )
    except ValueError as e:
        print("[!] Error: ", e)
        exit(1)
        
    try:
        # Display config
        print(" [*] Starting brute forcer.")
        print(" [*] Running attacks with %s workers" % args.concurrency)
        f.write(" [*] Testing... ")
        f.flush()
        
        # Run!
        credentials = run(config)
        
        if credentials is not None:
            print("\n [*] Credentials found!!\n")
            print(" " * 10, ">>  %s:%s  <<\n" % (credentials.user, credentials.password))
        else:
            print("\n [*] Credentials NOT found :(")
        print(" [*] Finished")
    except KeyboardInterrupt:
        print(" [*] Exiting")


if __name__ == "__main__" and __package__ is None:
    import sys
    import os
    
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, parent_dir)
    import ktcal2
    
    __package__ = str("ktcal2")
    del sys, os
    
    main()
