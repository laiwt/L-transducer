from string import Template
from L_Graph import *


class CodeGenerator:

    def __init__(self, l_graph):
        self.beginning = Template(open('./template/beginning.tmpl', 'r').read())
        self.main = Template(open('./template/main.tmpl', 'r').read())
        self.vertex = Template(open('./template/vertex.tmpl', 'r').read())
        self.edge = Template(open('./template/edge.tmpl', 'r').read())
        self.push = Template(open('./template/push.tmpl', 'r').read())
        self.pop = Template(open('./template/pop.tmpl', 'r').read())
        self.output = Template(open('./template/output.tmpl', 'r').read())
        self.toAnotherVertex = Template(open('./template/toAnotherVertex.tmpl', 'r').read())
        self.emptyInput = Template(open('./template/emptyInput.tmpl', 'r').read())
        self._continue = Template(open('./template/continue.tmpl', 'r').read())
        self._return = Template(open('./template/return.tmpl', 'r').read())
        self.exception = Template(open('./template/exception.tmpl', 'r').read())
        self.exception_end = Template(open('./template/exception_end.tmpl', 'r').read())
        self.code = []
        self.l_graph = l_graph
        self.in_stack = ['(', '[', '{', '<']
        self.out_stack = [')', ']', '}', '>']

    def generate(self):
        res_file = open('result.py', 'w')

        startVertexName = next(filter(lambda x: x.type == 'Start', self.l_graph.vertices)).name
        self.code.append(self.beginning.substitute(alphabet=str(self.l_graph.alphabet),start="'" + startVertexName + "'"))
        res_file.writelines(self.code)
        self.code.clear()

        for v in self.l_graph.vertices:
            self.code.append(self.vertex.substitute(vertex_name="'" + v.name + "'"))
            for e in v.edges:
                popped = False
                if e.input != '':
                    self.code.append(self.edge.substitute(symbol="'" + e.input + "'"))
                else:
                    if e.output != '':
                        self.code.append(self.emptyInput.substitute())
                if e.bracket != '':
                    if e.bracket[0] in self.in_stack:
                        self.code.append(self.push.substitute(symbol_in_stack="'" + e.bracket + "'"))
                    elif e.bracket[0] in self.out_stack:
                        i = self.out_stack.index(e.bracket[0])
                        self.code.append(self.pop.substitute(symbol_out_stack="'" + self.in_stack[i] + e.bracket[1:] + "'"))
                        popped = True
                if e.output != '':
                    if not popped:
                        self.code.append(self.output.substitute(indentation='',symbol_to_print="'" + e.output + "'"))
                    else:
                        self.code.append(self.output.substitute(indentation='    ',symbol_to_print="'" + e.output + "'"))
                if e.to != v:
                    if not popped:
                        self.code.append(self.toAnotherVertex.substitute(indentation='',new_vertex="'" + e.to.name + "'"))
                    else:
                        self.code.append(self.toAnotherVertex.substitute(indentation='    ',new_vertex="'" + e.to.name + "'"))
                if popped:
                    self.code.append(self._continue.substitute(indentation='    '))
                else:
                    self.code.append(self._continue.substitute(indentation=''))
            if v.type == 'End':
                self.code.append(self.exception_end.substitute())
                self.code.append(self._return.substitute())
            else:
                self.code.append(self.exception.substitute())
            res_file.writelines(self.code)
            self.code.clear()

        self.code.append(self.main.substitute())
        res_file.writelines(self.code)

        res_file.close()
        print('Code successfully generated!')


if __name__ == '__main__':
    l_graph = L_Graph()
    
    v1 = Vertex('1','start')
    v2 = Vertex('2','normal')
    v3 = Vertex('3','end')
    e11 = Edge(v1,'|','|','[')
    e12 = Edge(v2,'+','+')
    e22 = Edge(v2,'|','|','[')
    e23 = Edge(v3,'=','=')
    e33 = Edge(v3,'','|',']')
    v1.addEdge(e11)
    v1.addEdge(e12)
    v2.addEdge(e22)
    v2.addEdge(e23)
    v3.addEdge(e33)
    l_graph.addVertex(v1)
    l_graph.addVertex(v2)
    l_graph.addVertex(v3)

    # v1 = Vertex('1', 'start')
    # v2 = Vertex('2', 'end')
    # e111 = Edge(v1, '+', '+')
    # e112 = Edge(v1, '|', '|', '[')
    # e12 = Edge(v2, '=', '=')
    # e22 = Edge(v2, '', '|', ']')
    # v1.addEdge(e111)
    # v1.addEdge(e112)
    # v1.addEdge(e12)
    # v2.addEdge(e22)
    # l_graph.addVertex(v1)
    # l_graph.addVertex(v2)

    # v1 = Vertex('1', 'start')
    # v2 = Vertex('2', 'normal')
    # v3 = Vertex('3', 'end')
    # e121 = Edge(v2, 'a', '', '[a')
    # e122 = Edge(v2, 'b', '', '[b')
    # e123 = Edge(v2, 'c', '', '[c')
    # e221 = Edge(v2, 'a', 'a')
    # e222 = Edge(v2, 'b', 'b')
    # e223 = Edge(v2, 'c', 'c')
    # e231 = Edge(v3, '', 'a', ']a')
    # e232 = Edge(v3, '', 'b', ']b')
    # e233 = Edge(v3, '', 'c', ']c')
    # v1.addEdge(e121)
    # v1.addEdge(e122)
    # v1.addEdge(e123)
    # v2.addEdge(e221)
    # v2.addEdge(e222)
    # v2.addEdge(e223)
    # v2.addEdge(e231)
    # v2.addEdge(e232)
    # v2.addEdge(e233)
    # l_graph.addVertex(v1)
    # l_graph.addVertex(v2)
    # l_graph.addVertex(v3)

    generator = CodeGenerator(l_graph)
    generator.generate()