#!/usr/bin/python
# -*- coding: UTF-8, tab-width: 4 -*-

from sys import path as module_paths, stdin, stdout, argv
module_paths.insert(0, '../util')
from time import sleep
from log_util import log_ts

quiz = list(argv[1:])
if (len(quiz) > 0) and (quiz[0] == '--'):
    quiz.pop(0)
if len(quiz) == 1:
    quiz = quiz[0].split(', ')

log_ts('quiz start')
for question in quiz:
    log_ts('get ready for the question!')
    sleep(2)
    log_ts('asking:', question)
    stdout.write(question + '\n')
    stdout.flush()
    reply = stdin.readline()
    log_ts('got reply:', repr(reply))
log_ts('quiz end')
