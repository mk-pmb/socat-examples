#!/usr/bin/python
# -*- coding: UTF-8, tab-width: 4 -*-

from sys import stdin, stdout, stderr, argv
from os import getpid, getenv
from os.path import basename
import time


logname = basename(argv[0]).rsplit('.', 1)[0]
log_start_time = time.time()


def str_or_repr(x):
    try:
        return str(x)
    except:
        return repr(x)


def microsec_uptime(now = None):
    if now is None: now = time.time()
    return '{: 11.6f}'.format(now - log_start_time)


def microsec_walltime(now = None):
    if now is None: now = time.time()
    return time.strftime('%T', time.localtime(long(now))
        ) + '{:.6f}'.format(now % 1)[1:]


def log_ts(*args):
    now = microsec_uptime()
    stderr.write(' '.join(['[' + logname + ' ' + now + ']'
        ] + map(str_or_repr, args)) + '\n')
    stderr.flush()


def stdin_readline_loop(on_line):
    line_num = 0
    log_ts('listening on stdin.')
    while line_num is not None:
        input = stdin.readline()
        if input == '': break
        input = input.rstrip()
        line_num += 1
        if line_num == 1:
            if input.startswith('GET /'):
                if pseudo_cgi_fake_httpd(input, on_line):
                    return
        on_line(input)
    log_ts('got EOF on stdin.')


def pseudo_cgi_fake_httpd(input, on_line):
    input = input.split(' ')
    conn_info = { 'pid': getpid(), 'remote_ip': '' }
    if len(input) != 3: return False
    if input[2] not in ('HTTP/1.0', 'HTTP/1.1'): return false
    log_ts('Switching to HTTP mode.', conn_info)
    input = input[1].lstrip('/')
    while stdin.readline() not in ('', '\r\n', '\n'):
        pass
    try:
        result = on_line(input)
    except Exception as result:
        pass
    result = str_or_repr(result) + '\r\n'
    stdout.write('\r\n'.join(['200 OK',
        'Content-Type: text/plain',
        'Content-Length: ' + str(len(result)),
        'Connection: close',
        '', '', result]))
    stdout.flush()
    log_ts('Finished HTTP mode.', conn_info)
    return true
















# scroll
