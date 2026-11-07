import sys
import os

def run_bf(code, max_steps=1000000):
    code = ''.join(c for c in code if c in '><+-.,[]')
    
    mem = [0] * 30000
    ptr = 0
    code_ptr = 0
    steps = 0
    
    bracket_map = {}
    stack = []
    for i, cmd in enumerate(code):
        if cmd == '[':
            stack.append(i)
        elif cmd == ']':
            if not stack:
                sys.stderr.write(f"\nerro: colchete ] sem [ na posicao {i}\n")
                os._exit(1)
            start = stack.pop()
            bracket_map[start] = i
            bracket_map[i] = start
    
    if stack:
        sys.stderr.write(f"\nerro: colchetes nao balanceados\n")
        os._exit(1)
    
    while code_ptr < len(code) and steps < max_steps:
        cmd = code[code_ptr]
        
        if cmd == '>':
            ptr += 1
        elif cmd == '<':
            ptr -= 1
        elif cmd == '+':
            mem[ptr] = (mem[ptr] + 1) % 256
        elif cmd == '-':
            mem[ptr] = (mem[ptr] - 1) % 256
        elif cmd == '.':
            sys.stdout.write(chr(mem[ptr]))
        elif cmd == ',':
            c = sys.stdin.read(1)
            mem[ptr] = ord(c) if c else 0
        elif cmd == '[' and mem[ptr] == 0:
            code_ptr = bracket_map[code_ptr]
        elif cmd == ']' and mem[ptr] != 0:
            code_ptr = bracket_map[code_ptr]
        
        code_ptr += 1
        steps += 1
    
    sys.stdout.flush()

if __name__ == '__main__':
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            code = f.read()
        run_bf(code)
    finally:
        os._exit(0)