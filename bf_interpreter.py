import sys

def run_bf(code):
    mem = [0] * 30000
    ptr = 0
    code_ptr = 0
    output = []
    
    bracket_map = {}
    stack = []
    for i, cmd in enumerate(code):
        if cmd == '[':
            stack.append(i)
        elif cmd == ']':
            start = stack.pop()
            bracket_map[start] = i
            bracket_map[i] = start
    
    while code_ptr < len(code):
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
            output.append(chr(mem[ptr]))
        elif cmd == ',':
            mem[ptr] = ord(sys.stdin.read(1))
        elif cmd == '[':
            if mem[ptr] == 0:
                code_ptr = bracket_map[code_ptr]
        elif cmd == ']':
            if mem[ptr] != 0:
                code_ptr = bracket_map[code_ptr]
        
        code_ptr += 1
    
    return ''.join(output)

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        code = f.read()
    print(run_bf(code))