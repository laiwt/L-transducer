class Vertex:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.edges = []

    def addEdge(self, edge):
        self.edges.append(edge)


class Edge:
    bracket_list = ['(', ')', '[', ']', '{', '}', '<', '>']

    def __init__(self, to, input, output, brackets=''):
        self.to = to
        self.input = input
        self.output = output
        self.brackets = []
        temp = ''
        for c in brackets:
            if temp != '' and c in Edge.bracket_list:
                self.brackets.append(temp)
                temp = ''
            temp += c
        if temp != '':
            self.brackets.append(temp)


class L_Graph:
    open_dict = {'(': ')', '[': ']', '{': '}', '<': '>'}
    close_dict = {')': '(', ']': '[', '}': '{', '>': '<'}

    def __init__(self):
        self.vertices = []
        self.alphabet = ['\n']
        self.brackets = []
        self.stack_names = []

    def addVertex(self, vertex):
        self.vertices.append(vertex)
        for e in vertex.edges:
            if e.input != '' and not e.input in self.alphabet:
                self.alphabet.append(e.input)
            for b in e.brackets:
                if b not in self.brackets:
                    self.brackets.append(b)
    
    def check(self):
        for b in self.brackets:
            b_opposite = L_Graph.open_dict[b[0]] + b[1:] if b[0] in L_Graph.open_dict else L_Graph.close_dict[b[0]] + b[1:]
            if b_opposite not in self.brackets:
                return False
        return True
    
    def get_stack_name(self, s):
        return 'stack' + str(Edge.bracket_list.index(s[0]) // 2 + 1)
    
    def generate_stack_names(self):
        for s in self.brackets:
            stack_name = self.get_stack_name(s)
            if stack_name not in self.stack_names:
                self.stack_names.append(stack_name)
        self.stack_names.sort()