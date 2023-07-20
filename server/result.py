import sys

alphabet = ['\n', 'a', 'b', 'c']
end = False


def read_char():
    global end
    if not end:
        c = sys.stdin.read(1)
    else:
        return
    if c == '\n':
        end = True
    if not c in alphabet:
        raise Exception('\nError!Illegal character!')
    return c


def execute():
    s = '1'
    stack = []
    while True:
        if s == '1':
            c = read_char()
            if c == 'a':
                stack.append('[a')
                s = '2'
                continue
            if c == 'b':
                stack.append('[b')
                s = '2'
                continue
            if c == 'c':
                stack.append('[c')
                s = '2'
                continue
            raise Exception('\nError!Input not accepted!')
        if s == '2':
            c = read_char()
            if c == 'a':
                print('a', end='')
                continue
            if c == 'b':
                print('b', end='')
                continue
            if c == 'c':
                print('c', end='')
                continue
            if end:
                if stack[-1] == '[a':
                    stack.pop()
                    print('a', end='')
                    s = '3'
                    continue
            if end:
                if stack[-1] == '[b':
                    stack.pop()
                    print('b', end='')
                    s = '3'
                    continue
            if end:
                if stack[-1] == '[c':
                    stack.pop()
                    print('c', end='')
                    s = '3'
                    continue
            raise Exception('\nError!Input not accepted!')
        if s == '3':
            c = read_char()
            if not end:
                raise Exception('\nError!Input not accepted!')
            return


if __name__ == '__main__':
    execute()