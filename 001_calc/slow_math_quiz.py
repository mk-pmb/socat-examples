#!/usr/bin/python
# -*- coding: UTF-8, tab-width: 4 -*-

from sys import path as module_paths, stdin, stdout
module_paths.insert(0, '../util')
from time import sleep
from log_util import log_ts

formulae = [
    '1+1',
    '6*7',
    '42-23',
    ]

log_ts('quiz start')
for formula in formulae:
    log_ts('ready for a math question?')
    sleep(2)
    log_ts('asking:', formula)
    stdout.write(formula + '\n')
    stdout.flush()
    reply = stdin.readline()
    log_ts('got reply:', repr(reply))
log_ts('quiz end')
