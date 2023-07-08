class Vertex:

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.edges = []

    def addEdge(self, edge):
        self.edges.append(edge)


class Edge:

    def __init__(self, to, input, output, bracket=''):
        self.to = to
        self.input = input
        self.output = output
        self.bracket = bracket


class L_Graph:

    def __init__(self):
        self.vertices = []
        self.alphabet = ['\n']

    def addVertex(self, vertex):
        self.vertices.append(vertex)
        for e in vertex.edges:
            if e.input != '' and not e.input in self.alphabet:
                self.alphabet.append(e.input)