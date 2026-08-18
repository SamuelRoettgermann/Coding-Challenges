# 18 - Maximum path sum I  &&  67 - Maximum path sum II #
class Tree:
    root: "Node"

    class Node:
        val: int
        left: "Tree.Node"
        right: "Tree.Node"

        def __init__(self, val, left=None, right=None):
            self.val, self.left, self.right = val, left, right

        def __repr__(self):
            return f"{self.left.val if self.left else None}<-{self.val}->{self.right.val if self.right else None}"

    def __init__(self, root=None):
        self.root = root

    def __repr__(self):
        return repr(self.root)

    def __insert(self, nodes: list):
        """Expects len(nodes) = h(G) + 1
        After this operation all nodes in 'nodes' are leaves of the tree"""
        h = len(nodes) - 1
        if h == 0:  # empty tree case
            self.root = nodes[0]
            return

        layer = self.__get_level(h - 1)  # grab nodes from last layer
        for i in range(h):
            parent: "Tree.Node" = layer[i]
            parent.left, parent.right = nodes[i:i + 2]

    def __get_level(self, level) -> list:
        """Returns nodes at depth=level.
        Example returns:
            - level=0: [self.root]
            - level=1: [self.root.left, self.root.right]
            - ...
        """
        nodes = []

        def _helper(node, n, right_border):
            if n == 0:
                nodes.append(node)
            else:
                _helper(node.left, n - 1, False)
                if right_border:
                    _helper(node.right, n - 1, True)

        _helper(self.root, level, True)
        return nodes

    def __height(self):
        """Assumes this tree is full as it calculates the height by purely going through the left successors.+
        returns 0 for an empty tree, 1 for a tree with just a root, etc."""
        h = 0
        node = self.root
        while node is not None:
            h += 1
            node = node.left

        return h

    def print_tree(self):
        """prints the tree like it was given in the file (for debugging purposes)"""
        layers = [self.__get_level(i) for i in range(self.__height())]
        for layer in layers:
            print(' '.join(map(lambda node: f"{node.val:02}", layer)))

    @staticmethod
    def get_from_file(path) -> "Tree":
        """Reads and parses the triangle from a file at a given path"""
        T = Tree()

        with open(path) as f:
            lines = [line.split() for line in f.readlines()]
            for idx, line in enumerate(lines):
                cur_nodes = [Tree.Node(int(w)) for w in line]
                T.__insert(cur_nodes)

        return T

    def bfs(self):
        """Pseudo bfs as I was too stubborn to google how bfs exactly worked and now it's more like dfs"""
        highs: dict = {}

        def _helper(node, parent=None):
            if not node:  # if the parent is a leaf
                return

            x = highs.get(parent, 0) + node.val  # calculate the current path's score

            if x <= highs.get(node, 0):  # if the current node was already processed with a better path
                return

            highs[node] = x  # x is the best path
            _helper(node.left, node)
            _helper(node.right, node)

        _helper(self.root)

        return max(highs.values())


def benchmark(f):
    """Benchmarks a function f
    Should usually be used as a decorator"""
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        best = f(*args, **kwargs)
        total = time.time() - start
        return f"got {best} in {total:.8f} seconds"

    return wrapper


if __name__ == '__main__':
    t0 = Tree.get_from_file("euler18.txt")
    print(benchmark(t0.bfs)())

    t1 = Tree.get_from_file("euler67.txt")
    print(benchmark(t1.bfs)())