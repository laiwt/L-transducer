from string import Template
from L_Graph import *


class CodeGenerator:
    def __init__(self, l_graph):
        self.beginning = Template(open("./template/beginning.tmpl", "r").read())
        self.def_stack = Template(open("./template/def_stack.tmpl", "r").read())
        self.loop_start = Template(open("./template/loop_start.tmpl", "r").read())
        self.main = Template(open("./template/main.tmpl", "r").read())
        self.vertex = Template(open("./template/vertex.tmpl", "r").read())
        self.edge_condition = Template(
            open("./template/edge_condition.tmpl", "r").read()
        )
        self.undo_read = Template(open("./template/undo_read.tmpl", "r").read())
        self.push = Template(open("./template/push.tmpl", "r").read())
        self.pop = Template(open("./template/pop.tmpl", "r").read())
        self.output = Template(open("./template/output.tmpl", "r").read())
        self.toAnotherVertex = Template(
            open("./template/toAnotherVertex.tmpl", "r").read()
        )
        self._continue = Template(open("./template/continue.tmpl", "r").read())
        self.exception = Template(open("./template/exception.tmpl", "r").read())
        self.end = Template(open("./template/end.tmpl", "r").read())
        self.code = []
        self.l_graph = l_graph

    def get_condition(self, input, brackets, empty_edge=False, stack_dict=None, conditions=None, next_direct=()):
        if conditions == None:
            if (not empty_edge) and input == "":
                conditions = []
            else:
                conditions = ["c == '" + input + "'"]
        if stack_dict == None:
            stack_dict = {}
        for bracket in brackets:
            if bracket[0] in L_Graph.close_dict:
                stack_name = L_Graph.get_stack_name(bracket)
                if stack_name not in stack_dict:
                    stack_dict[stack_name] = 1
                else:
                    stack_dict[stack_name] += 1
                condition = "len(" + stack_name + ") > "
                pre = condition + str(stack_dict[stack_name] - 2)
                cur = condition + str(stack_dict[stack_name] - 1)
                try:
                    idx = conditions.index(pre)
                except ValueError:
                    conditions.append(cur)
                else:
                    conditions[idx] = cur
                if bracket[-1].isalnum():
                    condition = stack_name + "[-" + str(stack_dict[stack_name]) + "] == '" + bracket[-1] + "'"
                    conditions.append(condition)
        if next_direct != ():
            conditions.append("next() == '" + next_direct[0] + "'")
            return self.get_condition("", next_direct[1], stack_dict=stack_dict, conditions=conditions)
        return " and ".join(conditions)

    def generate_commands(
        self,
        vertex,
        edge,
        input,
        brackets,
        res_file,
        indentation="    ",
        empty_edge=False,
        unique=True,
    ):
        if empty_edge or input == "":
            self.code.append(self.undo_read.substitute(indentation=indentation))
        for bracket in brackets:
            if bracket[0] in L_Graph.open_dict:
                self.code.append(
                    self.push.substitute(
                        indentation=indentation,
                        stack_name=L_Graph.get_stack_name(bracket),
                        symbol=bracket[-1] if bracket[-1].isalnum() else "",
                    )
                )
            elif bracket[0] in L_Graph.close_dict:
                self.code.append(
                    self.pop.substitute(stack_name=L_Graph.get_stack_name(bracket))
                )
        if edge.output != "":
            self.code.append(
                self.output.substitute(indentation=indentation, symbol=edge.output)
            )
        if edge.to != vertex:
            self.code.append(
                self.toAnotherVertex.substitute(
                    indentation=indentation, new_vertex=edge.to.name
                )
            )
        if not (empty_edge and unique):
            self.code.append(self._continue.substitute())
        res_file.writelines(self.code)
        self.code.clear()

    def generate_if_block(self, vertex, edge, res_file, empty_edge=False, unique=True):
        if empty_edge:
            if unique:
                self.generate_commands(
                    vertex, edge, edge.input, edge.brackets, res_file, "", True
                )
            else:
                direct = self.l_graph.get_direct(edge)
                direct.sort(key=lambda x: len(x[1]), reverse=True)
                for d in direct:
                    condition = self.get_condition(d[0], d[1], True)
                    self.code.append(
                        self.edge_condition.substitute(condition=condition)
                    )
                    self.generate_commands(
                        vertex,
                        edge,
                        d[0],
                        d[1],
                        res_file,
                        empty_edge=True,
                        unique=False,
                    )
        else:
            if unique:
                condition = self.get_condition(edge.input, edge.brackets)
                self.code.append(self.edge_condition.substitute(condition=condition))
                self.generate_commands(
                    vertex, edge, edge.input, edge.brackets, res_file
                )
            else:
                direct = []
                for e in edge.to.edges:
                    direct.extend(self.l_graph.get_direct(e))
                if edge.to.type == "End":
                    direct.append(("", []))
                direct.sort(key=lambda x: len(x[1]), reverse=True)
                for d in direct:
                    condition = self.get_condition(edge.input, edge.brackets, next_direct=d)
                    self.code.append(
                        self.edge_condition.substitute(condition=condition)
                    )
                    self.generate_commands(
                        vertex, edge, edge.input, edge.brackets, res_file, unique=False
                    )

    def generate(self):
        # Generate the names of stacks.
        self.l_graph.check()
        self.l_graph.generate_stack_names()

        res_file = open("result.py", "w")

        # Generate the beginning of the code.
        startVertexName = self.l_graph.start.name
        self.code.append(
            self.beginning.substitute(
                alphabet=str(self.l_graph.alphabet), start=startVertexName
            )
        )
        res_file.writelines(self.code)
        self.code.clear()

        # Define stacks.
        for stack_name in self.l_graph.stack_names:
            self.code.append(self.def_stack.substitute(stack_name=stack_name))
        res_file.writelines(self.code)
        self.code.clear()

        # Loop starts.
        self.code.append(self.loop_start.substitute())
        res_file.writelines(self.code)
        self.code.clear()

        for v in self.l_graph.vertices:
            # self.l_graph.check_deterministic(v)
            self.code.append(self.vertex.substitute(vertex_name=v.name))
            res_file.writelines(self.code)
            self.code.clear()

            empty_edges = []
            edges_list = []
            empty_input_edges = []
            input_dict = {}
            for e in v.edges:
                if e.input != "":
                    edges_list.append(e)
                    if e.input not in input_dict:
                        input_dict[e.input] = 1
                    else:
                        input_dict[e.input] += 1
                else:
                    empty = True
                    for bracket in e.brackets:
                        if bracket[0] in L_Graph.close_dict:
                            empty = False
                            break
                    if empty:
                        empty_edges.append(e)
                        continue
                    else:
                        empty_input_edges.append(e)

            edges_list.extend(empty_input_edges)
            for edge in edges_list:
                unique = True
                if edge.input != "" and input_dict[edge.input] > 1:
                    unique = False
                self.generate_if_block(v, edge, res_file, False, unique)

            if v.type == "End":
                if len(empty_edges) > 0:
                    raise Exception("This may lead to non-determinism.")
                self.code.append(self.end.substitute())
            else:
                if len(empty_edges) > 0:
                    if len(empty_edges) == 1:
                        self.generate_if_block(v, empty_edges[0], res_file, True)
                    else:
                        for ee in empty_edges:
                            self.generate_if_block(v, ee, res_file, True, False)
                        self.code.append(self.exception.substitute())
                        res_file.writelines(self.code)
                        self.code.clear()
                else:
                    self.code.append(self.exception.substitute())
                    res_file.writelines(self.code)
                    self.code.clear()

        self.code.append(self.main.substitute())
        res_file.writelines(self.code)

        res_file.close()
        print("Code successfully generated!")


if __name__ == "__main__":
    l_graph = L_Graph()

    v1 = Vertex("1", "start")
    v2 = Vertex("2", "normal")
    v3 = Vertex("3", "end")
    e11 = Edge(v1, "|", "|", "[")
    e12 = Edge(v2, "+", "+")
    e22 = Edge(v2, "|", "|", "[")
    e23 = Edge(v3, "=", "=")
    e33 = Edge(v3, "", "|", "]")
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
