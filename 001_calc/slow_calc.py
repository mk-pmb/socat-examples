#!/usr/bin/python
# -*- coding: UTF-8, tab-width: 4 -*-

from sys import path as module_paths, stdout
module_paths.insert(0, '../util')
from log_util import log_ts, stdin_readline_loop
from time import sleep


def calc(input):
    formula = ''
    for ch in input:
        if ch in '0123456789.*+-/':
            formula += ch

    log_ts('received formula:', repr(formula))
    log_ts('pretending to calculate, please stand by!')
    sleep(0.5)
    try:
        result = str(eval(formula))
    except Exception as result:
        result = 'bad formula'
    log_ts('sending result:', repr(result))
    stdout.write(result + '\n')
    stdout.flush()


stdin_readline_loop(calc)
