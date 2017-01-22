#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from neovim import attach, setup_logging

setup_logging('pyplugin')
logger = logging.getLogger('pyplugin')

def main():

    if len(sys.argv)<=1:
        return

    servername = sys.argv[1]

    # connect neovim
    nvim = attach('socket', path=servername)

    nvim.command('echo "Hello world, pyplugin has started %s"' % nvim.channel_id)

    nvim.command('call pyplugin#rpc_started(%s)' % nvim.channel_id)

    while True:
        message = nvim.next_message()
        if message is None:
            logger.debug('stop: %s',message)
            break
        logger.debug('message: %s',message)

main()

