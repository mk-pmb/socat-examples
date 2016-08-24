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

log_ts('start')
sleep(2)
for formula in formulae:
    log_ts('asking:', formula)
    stdout.write(formula + '\n')
    stdout.flush()
    sleep(2)
log_ts('end')
