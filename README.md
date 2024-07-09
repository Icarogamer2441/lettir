# lettirlang
an open source programming language compiled with a built-from-scratch compiler.

# getting started
this language only supports compile to linux x86_64 at the moment
<br>
executing:
```console
python ./lettir.py -o [inputfile.let] [outputexec]
```
don't use the "[" and "]" this [] is only an example!<br>
you can use --asm to don't remove the assembly output file. example:
```console
python ./lettir.py -o example.let example --asm
```
you can only use the --asm after the '-o [inputfile.let] [outputexec]'!

## basics
to create functions you can use:
```lettir
fnc <name>
    <code...>
end
```

comments:
```lettir
fnc myfunc
    /* hello world! */
end
```
you can only create comments inside functions or macros
<br>

to create a main function you can use:
```lettir
fnc init
    0 exit
end
```

pushing numbers:
```lettir
fnc init
    10

    0 exit
end
```

printing integer numbers:
```lettir
fnc init
    10 print
    0 exit
end
```
ifs:
```lettir
fnc init
    10 5 > if
        50 print
    ifend

    0 exit
end
```
the code above checks if 10 is greater than 5, if it is true, it prints 50.<br>
duplicate top of stack:
```lettir
10 dup
```
stack: (10,10)
<br>
swap top of stack:
```lettir
10 20 swap
```
stack: (20,10)
<br>
printing the top of stack as ascii:
```lettir
65 cprint
```

## math
math is supported, you can use:
```lettir
10 5 -
```
to subtract 5 from 10, and get 5 as a result.<br>
and:
```lettir
10 5 +
```
to add 5 to 10, and get 15 as a result.<br>
# verifications
- ">" - greater than
- "<" - less than
- ">=" - greater than or equal to
- "<=" - less than or equal to
- "==" - equal to
- "!=" - not equal to
## whiles
whiles are supported, you can use:
```lettir
fnc init
    0 while
        dup 10 >= if
            stop
        ifend
        1 +
        dup print
    whend

    0 exit
end
```

## calling functions
```lettir
fnc test1
    10 print
end

fnc init
    test1

    0 exit
end
```
you can't use:
```lettir
fnc test1
    10
end

fnc init
    test1 print

    0 exit
end
```
because this won't work because the pushes are local (because of assembly)

## exit syscall
```lettir
fnc error
    5 print
    1 exit
end

fnc init
    error
end
```

# macros
with macros, you can do this:
```lettir
macro mymacro
    10
end

fnc init
    mymacro print

    0 exit
end
```

you can do function things with macros but the pushes are not local!
# strings
you can create strings!:
```lettir
include std.let

fnc init
    "Hello world!\n" puts
end
```

# or & and
you can do 'or' and 'and'. here an example with or:
```lettir
fnc init
    1 1 == 90 80 < or /* 1 == 1 or 90 < 80 */ if
        100 print
    ifend

    0 exit
end
```
and with 'and':
```lettir
fnc init
    1 1 == 90 80 > and /* 1 == 1 and 90 > 80 */ if
        100 print
    ifend

    0 exit
end
```

# variables
variables are here because they do not exist in the first version of this programming language. <br>
here an example:
```lettir
fnc init
    int n1 := 15
    n1 print

    string msg := Hello world!;
    
    11 msg 1 1 syscall
    10 cprint

    0 exit
end
```