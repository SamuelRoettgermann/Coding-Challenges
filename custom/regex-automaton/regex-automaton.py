class Regex:
    start: "Node"

    class Node:
        edges: dict[str | None, "Regex.Node"]
        end_state: bool

        def __init__(self, end_state=False):
            self.edges = {}
            self.end_state = end_state

        def advance(self, c: str):
            return self.edges.get(c, self.edges.get(None, None))

        def add_edge(self, s: str, node: "Regex.Node"):
            if s == '.':
                self.edges[None] = node

            self.edges[s] = node

        def set_end(self):
            self.end_state = True

        def is_end(self):
            return self.end_state

    def __init__(self, p: str):
        self.start = self.Node()
        self.__generate(p, self.start)

    def __generate(self, p: str, node: Node):
        if not p:
            node.set_end()
            return

        c, after_c = p[0], p[1:2]
        if after_c == '*':  # self-edge
            node.add_edge(c, node)
            self.__generate(p[2:], node)
        else:  # edge to new node
            next_node = self.Node()
            node.add_edge(c, next_node)
            self.__generate(p[1:], next_node)

    @staticmethod
    def compile(p: str):
        return Regex(p)

    def parse(self, s: str):
        node = self.start
        for c in s:
            if not (node := node.advance(c)):
                return False

        # return node.is_end()
        return node.is_end()


def match(s: str, p: str):
    # transform the pattern into an automata
    automata = Regex.compile(p)
    # parses the regex
    return automata.parse(s)


print(match("acddddedde", "a.*.d*e"))  # prints 'False'