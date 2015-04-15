#!/usr/bin/python

'''
Connect
Author: Philipp Schmitt <philipp.schmitt@post.lu>
'''


from __future__ import print_function
from pyVim.connect import Disconnect
from pyVim.connect import SmartConnect
from pyVmomi import vmodl
import atexit
import requests
import ssl
import sys
import traceback


'''
Custom exception that is be thrown when the connection to a vCenter failed
'''
class ConnectionError(Exception):
    pass


def connect(host, username, password, port=443, verify=False, debug=False):
    '''
    Connect to a vCenter via the API
    :param host: Hostname or IP of the vCenter
    :type host: str or unicode
    :param username: Username
    :type user: str or unicode
    :param password: Password
    :type user: str or unicode
    :param port: Port on which the vCenter API is running (default: 443)
    :type port: int
    :param verify: Whether to verify SSL certs upon connection (default: False)
    :type verify: bool
    :param debug: Debug option (default: False)
    :type debug: bool
    :return: Content
    :rtype: vim.ServiceInstanceContent
    '''

    if not verify:
        # Disable warnings about unsigned certificates
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings()

    try:
        si = None
        try:
            si = SmartConnect(
                host=host,
                user=username,
                pwd=password,
                port=port
            )
        except IOError as e:
            pass
        if not si:
            print('Connection could not be established', file=sys.stderr)
            raise ConnectionError()

        # Register auto disconnect
        atexit.register(Disconnect, si)
        # Return content
        return si.RetrieveContent()
    except vmodl.MethodFault as e:
        print('Caught vmodl fault: ', e.msg, file=sys.stderr)
        if debug:
            traceback.print_exc()
    except Exception as e:
        print('Caught exception:', str(e), file=sys.stderr)
        if debug:
            traceback.print_exc()
