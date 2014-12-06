# -*- coding: utf-8 -*-

"""
ktcal2: This file contains function for SSH brute forcer.
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

import asyncio
import asyncssh

from .data import FoundCredential

loop = None
result_user = None
result_password = None
counter = 1


@asyncio.coroutine
def _check_credentials(target, user, password, delay, sem_coroutines, port=22, display_func=None,
                       verbosity_level=0):
    """
    Check a concrete credential.
    
    :param target: target with SSH service running
    :type target: str

    :param password: password to test
    :type password: str

    :param sem_coroutines: Semaphore used to set maximum number of concurrent connections.
    :type sem_coroutines: Semaphore

    :param port: target port
    :type port: int
    """
    try:
        with (yield from sem_coroutines):
            global counter
            counter += 1

            if display_func is not None:
                if verbosity_level > 1:
                    msg = "\r [*] Testing... %s credentials (%s:%s)%s" % (counter, user, password, " " * 4)
                    display_func(msg)
                else:
                    msg = "\r [*] Testing... %s credentials%s" % (counter, " " * 4)
                    if counter % 4 == 0:
                        display_func(msg)

            conn, client = yield from asyncssh.create_connection(None,
                                                                 host=target,
                                                                 port=port,
                                                                 username=user,
                                                                 password=password,
                                                                 server_host_keys=None)

        # If not raise exception -> user/password found
        global result_password, result_user, loop
        result_user = user
        result_password = password

        loop.stop()
    except (asyncssh.misc.DisconnectError, ConnectionResetError):
        asyncio.sleep(delay)


# ----------------------------------------------------------------------
def ssh_check(params):
    """
    Try to find SSH credentials.
    
    :param params: GlobalParameters object 
    :type params: :class:`lib.data.GlobalParameters`
    
    :return: First valid credential in FoundCredential object
    :rtype: :class:`lib.data.FoundCredential`

    :raises: ConnectionError, ConnectionRefusedError
    """
    global loop

    try:
        sem_coroutines = asyncio.Semaphore(params.concurrency)
        user_list = params.user_list
        password_list = params.password_list
        target = params.target
        port = params.port
        delay = params.delay
        display_func = params.display_function
        verbosity = params.verbosity

        # Prepare event loop and create tasks
        loop = asyncio.get_event_loop()
        futures = [_check_credentials(target,
                                      user,
                                      password,
                                      delay,
                                      sem_coroutines,
                                      port,
                                      display_func,
                                      verbosity)
                   for user in user_list
                   for password in password_list]

        try:
            pass
            loop.run_until_complete(asyncio.wait(futures))
        except RuntimeError:
            # If some coroutine stops the loop, this exception will raise
            pass

        # Password found?
        if result_user is not None and result_password is not None:
            credential = FoundCredential(user=result_user, password=result_password)
        else:
            credential = None

        return credential

    except (OSError, asyncssh.Error) as exc:
        raise ConnectionError('SSH connection failed: ', str(exc))
    except ConnectionRefusedError:
        raise ConnectionRefusedError("Can't connect with remote host. Check IP and port")
