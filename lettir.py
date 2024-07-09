import sys
import subprocess
import os

partnum = [0]
functions = []
macros = {}
variables = {}

def search_lettirinclude(diretorio_atual):
    if 'lettirinclude' in os.listdir(diretorio_atual):
        return os.path.abspath(os.path.join(diretorio_atual, 'lettirinclude'))
    
    parent_dir = os.path.dirname(diretorio_atual)
    
    if parent_dir == diretorio_atual:
        return None
    
    return search_lettirinclude(parent_dir)

def comp(code, output, compile, islib, libpath):
    tokens = code.split()
    tokenpos = 1
    in_func = [False]
    funcname = [""]
    recentif = []
    recentwhile = []
    in_macro = [False]
    in_str = [False]
    finalstr = []
    in_comment = [False]
    macroname = [""]
    funccode = []

    def normalcode(codee):
        tokens = codee.split()
        tokenpos = 1
        while tokenpos <= len(tokens):
            token = tokens[tokenpos - 1]
            tokenpos += 1
            
            if not in_str[0] and not in_comment[0]:
                if token.isdigit() or (token.startswith("-") and token[1:].isdigit()):
                    out.write(f"  ;; push {token}\n")
                    out.write(f"  push {token}\n")
                elif token == "pop":
                    out.write(f"  ;; pop\n")
                    out.write(f"  pop rax\n")
                elif token == "+":
                    out.write("  ;; plus\n")
                    out.write("  pop rbx\n")
                    out.write("  pop rax\n")
                    out.write("  add rax, rbx\n")
                    out.write("  push rax\n")
                elif token == "-":
                    out.write("  ;; minus\n")
                    out.write("  pop rbx\n")
                    out.write("  pop rax\n")
                    out.write("  sub rax, rbx\n")
                    out.write("  push rax\n")
                elif token == "print":
                    partnum[0] += 1
                    out.write("  ;; print\n")
                    out.write(f"part_{partnum[0]}:\n")
                    out.write("  pop rax\n")
                    out.write("  mov rbx, buffer + 19\n")
                    out.write("  mov byte [rbx], 0x0A\n")
                    out.write("  mov rcx, 10\n")
                    out.write("  test rax, rax\n")
                    out.write(f"  js negative_{partnum[0]}\n")
                    out.write(f"convert_loop_{partnum[0]}:\n")
                    out.write("  xor rdx, rdx\n")
                    out.write("  div rcx\n")
                    out.write("  add dl, '0'\n")
                    out.write("  dec rbx\n")
                    out.write("  mov [rbx], dl\n")
                    out.write("  test rax, rax\n")
                    out.write(f"  jnz convert_loop_{partnum[0]}\n")
                    out.write(f"  jmp print_number_{partnum[0]}\n")
                    out.write(f"negative_{partnum[0]}:\n")
                    out.write("  neg rax\n")
                    out.write(f"convert_loop_neg_{partnum[0]}:\n")
                    out.write("  xor rdx, rdx\n")
                    out.write("  div rcx\n")
                    out.write("  add dl, '0'\n")
                    out.write("  dec rbx\n")
                    out.write("  mov [rbx], dl\n")
                    out.write("  test rax, rax\n")
                    out.write(f"  jnz convert_loop_neg_{partnum[0]}\n")
                    out.write("  dec rbx\n")
                    out.write("  mov byte [rbx], '-'\n")
                    out.write(f"print_number_{partnum[0]}:\n")
                    out.write("  mov rax, 1\n")
                    out.write("  mov rdi, 1\n")
                    out.write("  lea rsi, [rbx]\n")
                    out.write("  mov rdx, buffer + 20\n")
                    out.write("  sub rdx, rbx\n")
                    out.write("  syscall\n")
                elif token == "exit":
                    out.write("  ;; exit\n")
                    out.write("  mov rax, 60\n")
                    out.write("  pop rdi\n")
                    out.write("  syscall\n")
                elif token in functions:
                    out.write(f"  ;; call {token}\n")
                    out.write(f"  call {token}\n")
                elif token == "==":
                    partnum[0] += 1
                    out.write("  ;; ==\n")
                    out.write("  pop rbx\n")
                    out.write("  pop rax\n")
                    out.write("  cmp rax, rbx\n")
                    out.write(f"  jne not_equal_{partnum[0]}\n")
                    out.write("  push 1\n")
                    out.write(f"  jmp end_{partnum[0]}\n")
                    out.write(f"not_equal_{partnum[0]}:\n")
                    out.write("  push 0\n")
                    out.write(f"end_{partnum[0]}:\n")
                elif token == "!=":
                    partnum[0] += 1
                    out.write("  ;; !=\n")
                    out.write("  pop rbx\n")
                    out.write("  pop rax\n")
                    out.write("  cmp rax, rbx\n")
                    out.write(f"  je equal_{partnum[0]}\n")
                    out.write("  push 1\n")
                    out.write(f"  jmp end_{partnum[0]}\n")
                    out.write(f"equal_{partnum[0]}:\n")
                    out.write("  push 0\n")
                    out.write(f"end_{partnum[0]}:\n")
                elif token == "<":
                    partnum[0] += 1
                    out.write("  ;; <\n")
                    out.write("  pop rbx\n")
                    out.write("  pop rax\n")
                    out.write("  cmp rax, rbx\n")
                    out.write(f"  jge not_less_{partnum[0]}\n")
                    out.write("  push 1\n")
                    out.write(f"  jmp end_{partnum[0]}\n")
                    out.write(f"not_less_{partnum[0]}:\n")
                    out.write("  push 0\n")
                    out.write(f"end_{partnum[0]}:\n")
                elif token == ">":
                    partnum[0] += 1
                    out.write("  ;; >\n")
                    out.write("  pop rbx\n")
                    out.write("  pop rax\n")
                    out.write("  cmp rax, rbx\n")
                    out.write(f"  jle not_greater_{partnum[0]}\n")
                    out.write("  push 1\n")
                    out.write(f"  jmp end_{partnum[0]}\n")
                    out.write(f"not_greater_{partnum[0]}:\n")
                    out.write("  push 0\n")
                    out.write(f"end_{partnum[0]}:\n")
                elif token == "<=":
                    partnum[0] += 1
                    out.write("  ;; <=\n")
                    out.write("  pop rbx\n")
                    out.write("  pop rax\n")
                    out.write("  cmp rax, rbx\n")
                    out.write(f"  jg not_less_equal_{partnum[0]}\n")
                    out.write("  push 1\n")
                    out.write(f"  jmp end_{partnum[0]}\n")
                    out.write(f"not_less_equal_{partnum[0]}:\n")
                    out.write("  push 0\n")
                    out.write(f"end_{partnum[0]}:\n")
                elif token == ">=":
                    partnum[0] += 1
                    out.write("  ;; >=\n")
                    out.write("  pop rbx\n")
                    out.write("  pop rax\n")
                    out.write("  cmp rax, rbx\n")
                    out.write(f"  jl not_greater_equal_{partnum[0]}\n")
                    out.write("  push 1\n")
                    out.write(f"  jmp end_{partnum[0]}\n")
                    out.write(f"not_greater_equal_{partnum[0]}:\n")
                    out.write("  push 0\n")
                    out.write(f"end_{partnum[0]}:\n")
                elif token == "if":
                    partnum[0] += 1
                    out.write("  ;; if\n")
                    out.write("  pop rax\n")
                    out.write("  cmp rax, 1\n")
                    out.write(f"  je ifcode_{partnum[0]}\n")
                    out.write(f"  jmp end_{partnum[0]}\n")
                    out.write(f"ifcode_{partnum[0]}:\n")
                    recentif.append(partnum[0])
                elif token == "ifend":
                    ifnum = recentif.pop()
                    out.write(f"end_{ifnum}:\n")
                elif token == "while":
                    partnum[0] += 1
                    out.write("  ;; while\n")
                    out.write(f"whilecode_{partnum[0]}:\n")
                    recentwhile.append(partnum[0])
                elif token == "whend":
                    whilenum = recentwhile.pop()
                    out.write(f"  jmp whilecode_{whilenum}\n")
                    out.write(f"end_{whilenum}:\n")
                elif token == "stop":
                    whilenum = recentwhile.pop()
                    recentwhile.append(whilenum)
                    out.write("  ;; stop while\n")
                    out.write(f"  jmp end_{whilenum}\n")
                elif token == "dup":
                    out.write("  ;; dup\n")
                    out.write("  pop rax\n")
                    out.write("  push rax\n")
                    out.write("  push rax\n")
                elif token == "swap":
                    out.write("  ;; swap\n")
                    out.write("  pop rax\n")
                    out.write("  pop rbx\n")
                    out.write("  push rax\n")
                    out.write("  push rbx\n")
                elif token in macros.keys():
                    normalcode(" ".join(macros[token]))
                elif token == "cprint":
                    out.write("  ;; cprint\n")
                    out.write("  pop rax\n")
                    out.write("  mov [buffer], rax\n")
                    out.write("  mov rsi, buffer\n")
                    out.write("  mov rdx, 1\n")
                    out.write("  mov rax, 1\n")
                    out.write("  mov rdi, 1\n")
                    out.write("  syscall\n")
                elif token.startswith("\""):
                    if token.endswith("\""):
                        finalstr.append(token.replace("\"", "").replace("\\n", "\n").replace("/n", "\\n"))
                        out.write("  push 0\n")
                        for letter in " ".join(finalstr)[::-1]:
                            out.write(f"  push {ord(letter)}\n")
                        finalstr.clear()
                    else:
                        finalstr.append(token.replace("\"", "").replace("\\n", "\n").replace("/n", "\\n"))
                        in_str[0] = True
                elif token == "/*":
                    in_comment[0] = True
                elif token == "or":
                    out.write("  ;; or\n")
                    out.write("  pop rbx\n")
                    out.write("  pop rax\n")
                    out.write("  or rax, rbx\n")
                    out.write("  push rax\n")
                elif token == "and":
                    out.write("  ;; and\n")
                    out.write("  pop rbx\n")
                    out.write("  pop rax\n")
                    out.write("  and rax, rbx\n")
                    out.write("  push rax\n")
                elif token == "int":
                    partnum[0] += 1
                    token = tokens[tokenpos - 1]
                    name = token
                    tokenpos += 1
                    token = tokens[tokenpos - 1]
                    tokenpos += 1
                    if token == ":=":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        out.write("  ;; int var\n")
                        out.write("section .data\n")
                        out.write(f"  {name} dq {int(token)}\n")
                        out.write("section .text\n")
                        out.write(f"part_{partnum[0]}:\n")
                        variables[name] = "int"
                    else:
                        print("Error: use ':=' to atribute variable values")
                        sys.exit(1)
                elif token == "string":
                    partnum[0] += 1
                    token = tokens[tokenpos - 1]
                    name = token
                    tokenpos += 1
                    token = tokens[tokenpos - 1]
                    tokenpos += 1
                    if token == ":=":
                        finalvalue = []
                        while tokenpos <= len(tokens):
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token.endswith(";"):
                                finalvalue.append(token.replace(";", ""))
                                out.write("  ;; str var\n")
                                out.write("section .data\n")
                                out.write(f'  {name} db \'{" ".join(finalvalue)}\', 0\n')
                                out.write("section .text\n")
                                out.write(f"part_{partnum[0]}:\n")
                                variables[name] = "str"
                                break
                            else:
                                finalvalue.append(token)
                    else:
                        print("Error: use ':=' to atribute variable values")
                        sys.exit(1)
                elif token in variables.keys():
                    if variables[token] == "int":
                        out.write("  ;; int var push\n")
                        out.write(f"  mov rax, [{token}]\n")
                        out.write(f"  push rax\n")
                    elif variables[token] == "str":
                        out.write("  ;; str var push\n")
                        out.write(f"  push {token}\n")
                    else:
                        print("Error: unknown variable type to push.")
                        sys.exit(1)
                elif token == "syscall":
                    out.write("  ;; syscall\n")
                    out.write("  pop rax\n")
                    out.write("  pop rdi\n")
                    out.write("  pop rsi\n")
                    out.write("  pop rdx\n")
                    out.write("  syscall")
                else:
                    print(f"Error: unknown keyword: {token}")
                    sys.exit(1)
            elif in_str[0]:
                if token.endswith("\""):
                    finalstr.append(token.replace("\"", "").replace("\\n", "\n").replace("/n", "\\n"))
                    out.write("  push 0\n")
                    for letter in " ".join(finalstr)[::-1]:
                        out.write(f"  push {ord(letter)}\n")
                    finalstr.clear()
                    in_str[0] = False
                else:
                    finalstr.append(token.replace("\"", "").replace("\\n", "\n").replace("/n", "\\n"))
            elif in_comment[0]:
                if token == "*/":
                    in_comment[0] = False
                else:
                    pass

    if not islib:
        with open(f"{output}.asm", "w") as outt:
            outt.write("section .data\n")
            outt.write("  digits db '0123456789'\n")
            outt.write("  nl db 10, 0\n")
            outt.write("section .bss\n")
            outt.write("  buffer resb 20\n")
            outt.write("section .text\n")
            outt.write("  global _start\n")
        with open(f"{output}.asm", "a") as out:
            while tokenpos <= len(tokens):
                token = tokens[tokenpos - 1]
                tokenpos += 1

                if not in_func[0] and not in_macro[0]:
                    if token == "fnc":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token == "init":
                            out.write(f"_start:\n")
                        elif token == "_start":
                            print("Error: use 'init' function name to set main function.")
                            sys.exit(1)
                        else:
                            out.write(f"{token}:\n")
                            functions.append(token)
                        in_func[0] = True
                        funcname[0] = token
                    elif token == "macro":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        in_macro[0] = True
                        macroname[0] = token
                        macros[token] = []
                    elif token == "include":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token.endswith(".let"):
                            with open(f"{libpath}/{token}", "r") as lib:
                                comp(lib.read(), output, False, True, libpath)
                        else:
                            print("Error: use .let file extension to import librarys.")
                            sys.exit(1)
                elif in_func[0]:
                    if token == "end":
                        in_func[0] = False
                        if funcname[0] == "init":
                            normalcode(" ".join(funccode))
                            funccode.clear()
                        else:
                            normalcode(" ".join(funccode))
                            out.write("  ret\n")
                            funccode.clear()
                    else:
                        funccode.append(token)
                elif in_macro[0]:
                    if token == "end":
                        in_macro[0] = False
                    else:
                        macros[macroname[0]].append(token)
    elif islib:
        with open(f"{output}.asm", "a") as out:
            while tokenpos <= len(tokens):
                token = tokens[tokenpos - 1]
                tokenpos += 1

                if not in_func[0] and not in_macro[0]:
                    if token == "fnc":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token == "init":
                            out.write(f"_start:\n")
                        elif token == "_start":
                            print("Error: use 'init' function name to set main function.")
                            sys.exit(1)
                        else:
                            out.write(f"{token}:\n")
                            functions.append(token)
                        in_func[0] = True
                        funcname[0] = token
                    elif token == "macro":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        in_macro[0] = True
                        macroname[0] = token
                        macros[token] = []
                    elif token == "include":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token.endswith(".let"):
                            with open(f"{libpath}/{token}", "r") as lib:
                                comp(lib.read(), output, False, True, libpath)
                        else:
                            print("Error: use .let file extension to import librarys.")
                            sys.exit(1)
                elif in_func[0]:
                    if token == "end":
                        in_func[0] = False
                        if funcname[0] == "init":
                            normalcode(" ".join(funccode))
                            funccode.clear()
                        else:
                            normalcode(" ".join(funccode))
                            out.write("  ret\n")
                            funccode.clear()
                    else:
                        funccode.append(token)
                elif in_macro[0]:
                    if token == "end":
                        in_macro[0] = False
                    else:
                        macros[macroname[0]].append(token)

    if compile:
        subprocess.run(f"nasm -f elf64 -o {output}.o {output}.asm", shell=True)
        subprocess.run(f"ld -o {output} {output}.o", shell=True)

if __name__ == "__main__":
    version = "1.2"
    print(f"Lettir version: {version}")
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} -o [input file] [output file]")
    else:
        if sys.argv[1] == "-o":
            if len(sys.argv) < 3:
                print(f"Usage: {sys.argv[0]} -o [input file] [output file]")
            else:
                compile = True
                inputfile = sys.argv[2]
                outputfile = sys.argv[3]
                currentdir = os.getcwd()
                if inputfile.endswith(".let"):
                    with open(inputfile, "r") as inpf:
                        comp(inpf.read(), outputfile, compile, False, search_lettirinclude(currentdir))
                    if "--asm" in sys.argv:
                        pass
                    else:
                        subprocess.run(f"rm -rf {outputfile}.o {outputfile}.asm", shell=True)
                else:
                    print("Error: use .let file extension.")
                    sys.exit(1)
