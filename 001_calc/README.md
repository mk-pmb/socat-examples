
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
A leading `#` at marks explanations or suggested interaction.

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

First have a look at what our math quiz will send to its stdout.
```
$ ./slow_math_quiz.py
[slow_math_quiz    0.000013] start
[slow_math_quiz    2.000833] asking: 1+1
1+1
[slow_math_quiz    4.002997] asking: 6*7
6*7
[slow_math_quiz    6.005180] asking: 42-23
42-23
[slow_math_quiz    8.007338] end
```

Let's connect that to our calculator!

```
$ socat EXEC:./slow_math_quiz.py EXEC:./slow_calc.py
[slow_calc    0.000014] start
[slow_math_quiz    0.000013] start
[slow_math_quiz    2.002117] asking: 1+1
[slow_calc    2.002471] received formula: '1+1'
[slow_calc    2.002521] pretending to calculate, please stand by!
[slow_calc    2.503147] sending result: '2'
[slow_math_quiz    4.004337] asking: 6*7
[slow_calc    4.004650] received formula: '6*7'
[slow_calc    4.004708] pretending to calculate, please stand by!
[slow_calc    4.505415] sending result: '42'
[slow_math_quiz    6.006522] asking: 42-23
[slow_calc    6.006791] received formula: '42-23'
[slow_calc    6.006837] pretending to calculate, please stand by!
[slow_calc    6.507523] sending result: '19'
[slow_math_quiz    8.008703] end
[slow_calc    8.012468] end
```


TCP server <—> program
----------------------

Let's connect our calculator to a TCP port, accepting one single connection.
We'll also add two `-d` options to have socat report some of its own activity.
You'll nee two shells (easiest way: two terminal windows) for this example.
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

  * Try swapping the connection ends in the socat commands.
    (In the first example, that would put the program first and STDIO last.)
    These simple examples should work in both directions,
    so they should behave the same even if swapped.













