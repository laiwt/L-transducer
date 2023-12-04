alphabet = ['a', 'b']
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
    stack2 = []
    while True:
        if s == '1':
            c = read_char()
            if c == 'a':
                stack2.append('')
                continue
            undo_read()
            s = '2'
        if s == '2':
            c = read_char()
            if c == '' and len(stack2) > 0:
                undo_read()
                stack2.pop()
                s = '3'
                continue
            if c == 'b':
                continue
            if c == 'b' and len(stack2) > 0:
                stack2.pop()
                continue
            raise Exception('Error!Input not accepted!')
        if s == '3':
            c = read_char()
            if len(stack2) > 0:
                undo_read()
                stack2.pop()
                print('a', end='')
                continue
            if c != '':
                raise Exception('Error!Input not accepted!')
            return


if __name__ == '__main__':
    try:
        execute()
    except Exception as e:
        print(e)