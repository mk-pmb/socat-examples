
Calculator examples
===================

Here you have two dummy programs whose best feature is that they log
timestamps of when they do what, so you can watch their interaction.

stdio <—> program
-----------------

Let's start by connecting your terminal to the calculator program.
You wouldn't need `socat` for that, you could just execute the
program directly of course. It will become more interesting when
we change one side of the connection – soon.

Lines that start with `$` are shell commands.
A leading `#` marks explanations or suggested interaction.

```
$ socat STDIO EXEC:./slow_calc.py
[slow_calc    0.000013] start
# Try typing some formula, e.g. "5+10":
5+10
[slow_calc    2.064822] received formula: '5+10'
[slow_calc    2.064878] pretending to calculate, please stand by!
[slow_calc    2.565559] sending result: '15'
15
# Try a non-formula, e.g. "hello":
hello
[slow_calc    6.208739] received formula: ''
[slow_calc    6.208809] pretending to calculate, please stand by!
[slow_calc    6.709481] sending result: 'bad formula'
bad formula
# press Ctrl-d to send EOF on stdin
[slow_calc   14.816567] end
```


program <—> program
-------------------

First take the math quiz yourself to see what it does.
It won't judge your answers anyway. ;-)
```
$ ./math_quiz.sh
[slow_quiz    0.000013] quiz start
[slow_quiz    0.000072] get ready for the question!
# And about 2 seconds later:
[slow_quiz    2.002197] asking: 1+1
1+1
# Now type an answer. You've probably guessed this one already:
2
[slow_quiz    3.552008] got reply: '2\n'
[slow_quiz    3.552073] get ready for the question!
[slow_quiz    5.553415] asking: 6*7
6*7
# Halfway done! In order to not spoil your riddle fun, I'll just type…
foo
[slow_quiz    7.391817] got reply: 'foo\n'
[slow_quiz    7.391905] get ready for the question!
[slow_quiz    9.393975] asking: 42-23
42-23
# Once again, not spoiling:
bar
[slow_quiz   10.624081] got reply: 'bar\n'
[slow_quiz   10.624145] quiz end
```

Now let's cheat big and connect our calculator to it!

```
$ socat EXEC:./math_quiz.sh EXEC:./slow_calc.py
[slow_quiz    0.000014] quiz start
[slow_quiz    0.000078] get ready for the question!
[slow_calc    0.000015] listening on stdin.
[slow_quiz    2.002195] asking: 1+1
[slow_calc    2.002435] received formula: '1+1'
[slow_calc    2.002479] pretending to calculate, please stand by!
[slow_calc    2.503191] sending result: '2'
[slow_quiz    2.503448] got reply: '2\n'
[slow_quiz    2.503523] get ready for the question!
[slow_quiz    4.505598] asking: 6*7
[slow_calc    4.505737] received formula: '6*7'
[slow_calc    4.505789] pretending to calculate, please stand by!
[slow_calc    5.006493] sending result: '42'
[slow_quiz    5.006713] got reply: '42\n'
[slow_quiz    5.006754] get ready for the question!
[slow_quiz    7.008857] asking: 42-23
[slow_calc    7.009029] received formula: '42-23'
[slow_calc    7.009085] pretending to calculate, please stand by!
[slow_calc    7.509797] sending result: '19'
[slow_quiz    7.510024] got reply: '19\n'
[slow_quiz    7.510082] quiz end
[slow_calc    7.514706] got EOF on stdin.
```


TCP server <—> program
----------------------

Let's connect our calculator to a TCP port, accepting one single connection.
I'll use port 4321 but you can pick your own just as well.

We'll also add two `-d` options to have socat report some of its own activity.

You'll nee two shells for this example.
The easiest way is to open two terminal windows.
We'll call one of them "server" and the other one "client".

```
# @ server:
$ socat -d -d TCP4-LISTEN:4321 EXEC:./slow_calc.py
socat[15984] N listening on AF=2 0.0.0.0:4321
# @ client:
$ socat -d -d STDIO TCP4:localhost:4321
socat[20398] N reading from and writing to stdio
socat[20398] N opening connection to AF=2 127.0.0.1:4321
socat[20398] N successfully connected from local address AF=2 127.0.0.1:35344
socat[20398] N starting data transfer loop with FDs [0,1] and [3,3]
# @ server:
socat[20315] N accepting connection from AF=2 127.0.0.1:35344 on AF=2 127.0.0.1:4321
socat[20315] N forking off child, using socket for reading and writing
socat[20315] N forked off child process 20400
socat[20315] N forked off child process 20400
socat[20315] N starting data transfer loop with FDs [4,4] and [3,3]
socat[20400] N execvp'ing "./slow_calc.py"
[slow_calc    0.000014] listening on stdin.
# @ client: type a formula, e.g. "11*12":
11*12
# @ server:
[slow_calc   68.617277] received formula: '11*12'
[slow_calc   68.617343] pretending to calculate, please stand by!
[slow_calc   69.118035] sending result: '132'
# @ client:
132
# Try a bit more if you like; then send EOF to the client (press Ctrl-d):
socat[20398] N socket 1 (fd 0) is at EOF
socat[20398] N socket 1 (fd 0) is at EOF
socat[20398] N socket 2 (fd 3) is at EOF
socat[20398] N exiting with status 0
# @ server:
socat[20315] N socket 1 (fd 4) is at EOF
[slow_calc  129.017152] got EOF on stdin.
socat[20315] N socket 1 (fd 4) is at EOF
socat[20315] N socket 2 (fd 3) is at EOF
socat[20315] N exiting with status 0
```

That's it for the first lesson. We'll do more TCP next time!


Exercises
---------
  * Modify the TCP example: In the client terminal,
    connect the math quiz program instead of STDIO.

  * Change the questions in `math_quiz.sh` and answer it over TCP.

  * Try swapping the connection ends in the socat commands.
    (In the first example, that would put the program first and STDIO last.)
    These simple examples should work in both directions,
    so they should behave the same even if swapped.













