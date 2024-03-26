alphabet = ['|', '0', '1']
idx = -1
input_str = ''

def read_char():
    global idx
    idx += 1
    if idx < len(input_str):
        c = input_str[idx]
    else:
        return ''
    if not c in alphabet:
        raise Exception('Error!Illegal character!')
    return c

def undo_read():
    global idx
    if idx < len(input_str):
        idx -= 1

def execute():
    global input_str
    input_str = input()
    s = '1'
    stack1 = []
    stack2 = []
    stack5 = []
    stack6 = []
    stack7 = []
    while True:
        if s == '1':
            c = read_char()
            if c == '|':
                stack5.append('|')
                stack7.append('1')
                s = '2'
                continue
            if c == '0':
                stack5.append('0')
                stack7.append('0')
                s = '2'
                continue
            if c == '1':
                stack5.append('1')
                stack7.append('0')
                s = '2'
                continue
            if len(stack6) > 0 and stack6[-1] == '|':
                undo_read()
                stack6.pop()
                stack5.append('|')
                stack7.append('1')
                s = '2'
                continue
            if len(stack6) > 0 and stack6[-1] == '0':
                undo_read()
                stack6.pop()
                stack5.append('0')
                stack7.append('0')
                s = '2'
                continue
            if len(stack6) > 0 and stack6[-1] == '1':
                undo_read()
                stack6.pop()
                stack5.append('1')
                stack7.append('0')
                s = '2'
                continue
            undo_read()
            stack6.append('0')
            stack7.append('0')
            s = '3'
        if s == '2':
            c = read_char()
            if c == '|':
                stack5.append('|')
                continue
            if c == '0':
                stack5.append('0')
                continue
            if c == '1':
                stack5.append('1')
                continue
            if len(stack6) > 0 and stack6[-1] == '|':
                undo_read()
                stack6.pop()
                stack5.append('|')
                continue
            if len(stack6) > 0 and stack6[-1] == '0':
                undo_read()
                stack6.pop()
                stack5.append('0')
                continue
            if len(stack6) > 0 and stack6[-1] == '1':
                undo_read()
                stack6.pop()
                stack5.append('1')
                continue
            undo_read()
            s = '3'
        if s == '3':
            c = read_char()
            undo_read()
            s = '10'
        if s == '4':
            c = read_char()
            if len(stack6) > 0 and stack6[-1] == '|':
                undo_read()
                stack6.pop()
                s = '5'
                continue
            raise Exception('Error!Input not accepted!')
        if s == '5':
            c = read_char()
            if len(stack6) > 0 and stack6[-1] == '|':
                undo_read()
                stack6.pop()
                stack5.append('|')
                continue
            if len(stack6) > 0 and stack6[-1] == '0':
                undo_read()
                stack6.pop()
                stack2.append('0')
                s = '6'
                continue
            if len(stack6) > 0 and stack6[-1] == '1':
                undo_read()
                stack6.pop()
                stack2.append('1')
                s = '6'
                continue
            undo_read()
            stack2.append('0')
            s = '7'
        if s == '6':
            c = read_char()
            if len(stack6) > 0 and stack6[-1] == '0':
                undo_read()
                stack6.pop()
                stack2.append('0')
                continue
            if len(stack6) > 0 and stack6[-1] == '1':
                undo_read()
                stack6.pop()
                stack2.append('1')
                continue
            undo_read()
            s = '7'
        if s == '7':
            c = read_char()
            if len(stack2) > 0 and stack2[-1] == '1':
                undo_read()
                stack2.pop()
                stack1.append('0')
                continue
            if len(stack2) > 0 and stack2[-1] == '0':
                undo_read()
                stack2.pop()
                stack1.append('1')
                s = '8'
                continue
            undo_read()
            stack1.append('1')
            s = '9'
        if s == '8':
            c = read_char()
            if len(stack2) > 0 and stack2[-1] == '0':
                undo_read()
                stack2.pop()
                stack1.append('0')
                continue
            if len(stack2) > 0 and stack2[-1] == '1':
                undo_read()
                stack2.pop()
                stack1.append('1')
                continue
            undo_read()
            s = '9'
        if s == '9':
            c = read_char()
            if len(stack1) > 0 and stack1[-1] == '0':
                undo_read()
                stack1.pop()
                stack5.append('0')
                continue
            if len(stack1) > 0 and stack1[-1] == '1':
                undo_read()
                stack1.pop()
                stack5.append('1')
                continue
            undo_read()
            s = '12'
        if s == '10':
            c = read_char()
            if len(stack5) > 0 and stack5[-1] == '|':
                undo_read()
                stack5.pop()
                stack6.append('|')
                continue
            if len(stack5) > 0 and stack5[-1] == '0':
                undo_read()
                stack5.pop()
                stack6.append('0')
                continue
            if len(stack5) > 0 and stack5[-1] == '1':
                undo_read()
                stack5.pop()
                stack6.append('1')
                continue
            if len(stack7) > 0 and stack7[-1] == '1':
                undo_read()
                stack7.pop()
                s = '4'
                continue
            if len(stack7) > 0 and stack7[-1] == '0':
                undo_read()
                stack7.pop()
                s = '11'
                continue
            raise Exception('Error!Input not accepted!')
        if s == '11':
            c = read_char()
            if len(stack6) > 0 and stack6[-1] == '0':
                undo_read()
                stack6.pop()
                print('0', end='')
                continue
            if len(stack6) > 0 and stack6[-1] == '1':
                undo_read()
                stack6.pop()
                print('1', end='')
                continue
            if c != '' or len(stack1) != 0 or len(stack2) != 0 or len(stack5) != 0 or len(stack6) != 0 or len(stack7) != 0:
                raise Exception('Error!Input not accepted!')
            return
        if s == '12':
            c = read_char()
            if len(stack5) > 0 and stack5[-1] == '0':
                undo_read()
                stack5.pop()
                stack6.append('0')
                continue
            if len(stack5) > 0 and stack5[-1] == '1':
                undo_read()
                stack5.pop()
                stack6.append('1')
                continue
            if len(stack5) > 0 and stack5[-1] == '|':
                undo_read()
                stack5.pop()
                stack6.append('|')
                continue
            undo_read()
            s = '1'


if __name__ == '__main__':
    try:
        execute()
    except Exception as e:
        print('\n' + str(e))