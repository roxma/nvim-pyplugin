#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
from neovim import attach, setup_logging

def getLogger():

    logger = logging.getLogger(__name__)

    level = logging.INFO
    if 'NVIM_PYTHON_LOG_LEVEL' in os.environ:
        # use nvim's logging
        setup_logging('pyplugin')
        l = getattr(logging,
                os.environ['NVIM_PYTHON_LOG_LEVEL'].strip(),
                level)
        if isinstance(l, int):
            level = l
    elif 'DEBUG' in os.environ:
        logfile = 'pyplugin.log'
        handler = logging.FileHandler(logfile, 'w')
        handler.formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s @ '
            '%(filename)s:%(funcName)s:%(lineno)s] %(process)s - %(message)s')
        logging.root.addHandler(handler)
        level = logging.DEBUG
        logger.setLevel(level)
    logger.setLevel(level)

    return logger

logger = getLogger()


# env
# NVIM_PYTHON_LOG_FILE
# NVIM_PYTHON_LOG_LEVEL
# 
# NVIM_PYTHON_LOG_FILE=nvim.log NVIM_PYTHON_LOG_LEVEL=INFO nvim

def main():

    if len(sys.argv)<=1:
        return

    servername = sys.argv[1]

    # connect neovim
    nvim = attach('socket', path=servername)

    nvim.command('echom "pyplugin started, channel id %s"' % nvim.channel_id)

    nvim.command('call pyplugin#rpc_started(%s)' % nvim.channel_id)

    # # no screen this large
    # nvim.ui_attach(512, 512, False)

    while True:
        message = nvim.next_message()
        if message is None:
            logger.info('stop: %s',message)
            break
        logger.info('message: %s',message)

main()

