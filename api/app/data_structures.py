from typing import Any

class LinkedListNode:
    def __init__(
        self,
        val: int = 0,
        next: LinkedListNode | None = None,
        prev: LinkedListNode | None = None,
        key: int = 0,
        random: LinkedListNode | None = None,
    ):
        self.val = val
        self.next = next
        self.prev = prev
        self.key = key
        self.random = random

    def _encode_linked_list(self) -> str:
        vals = []
        visited = {} # {node: pos}
        curr = self
        while curr:
            if curr in visited:
                vals.append(f"{visited[curr]}*")
                break
            vals.append(str(curr.val))
            curr = curr.next
            visited[curr] = len(visited)
        return f"L[{','.join(vals)}]"

    def __str__(self):
        return self._encode_linked_list()

def _decode_linked_list(input: str) -> LinkedListNode | None:
    vals_raw = input[2:-1]
    if not vals_raw:
        return None

    vals = vals_raw.split(',')
    has_cycle = vals[-1].endswith('*')
    pos = int(vals.pop()[:-1]) if has_cycle else -1

    dummy = curr = LinkedListNode()
    nodes = []
    for val in vals:
        curr.next = LinkedListNode(int(val))
        curr = curr.next
        nodes.append(curr)

    if pos != -1:
        curr.next = nodes[pos]

    return dummy.next

class BinaryTreeNode:
    def __init__(
        self,
        val: int = 0,
        left: BinaryTreeNode | None = None,
        right: BinaryTreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right

    # level-order where only non-None nodes add children, and trailing None's are trimmed
    def _encode_binary_tree(self) -> str:
        res = []
        q = [self]

        for node in q:
            if node:
                res.append(str(node.val))
                q.append(node.left)
                q.append(node.right)
            else:
                res.append('N')

        while res and res[-1] == 'N':
            res.pop()

        return f"T[{','.join(res)}]"

    def __str__(self):
        return self._encode_binary_tree()

def _decode_binary_tree(input: str) -> BinaryTreeNode | None:
    vals_raw = input[2:-1]
    if not vals_raw:
        return None

    vals = vals_raw.split(',')
    root = BinaryTreeNode(int(vals[0]))
    q = [root]

    i = 1
    for node in q:
        if i < len(vals):
            if vals[i] != 'N':
                node.left = BinaryTreeNode(int(vals[i]))
                q.append(node.left)
            i += 1

        if i < len(vals):
            if vals[i] != 'N':
                node.right = BinaryTreeNode(int(vals[i]))
                q.append(node.right)
            i += 1

    return root

class QuadTreeNode:
    def __init__(
        self,
        is_leaf: bool = False,
        val: bool = 0,
        top_left: QuadTreeNode | None = None,
        top_right: QuadTreeNode | None = None,
        bottom_left: QuadTreeNode | None = None,
        bottom_right: QuadTreeNode | None = None
    ):
        self.is_leaf = is_leaf
        self.val = val
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right

    def _encode_quad_tree(self):
        res = []
        q = [self]
        for node in q:
            res.append(f"[{int(node.is_leaf)},{int(node.val)}]")
            if not node.is_leaf:
                q.extend([node.top_left, node.top_right, node.bottom_left, node.bottom_right])
        return f"Q[{','.join(res)}]"

    def __str__(self):
        return self._encode_quad_tree()

def _decode_quad_tree(input: str) -> QuadTreeNode | None:
    def mk_node(pair: str) -> QuadTreeNode:
        leaf_str, val_str = pair.split(',')
        return QuadTreeNode(bool(int(val_str)), bool(int(leaf_str)))

    if input == "Q[]":
        return None

    pairs_raw = input[3:-2]
    if not pairs_raw:
        return None

    pairs = pairs_raw.split("],[")
    root = mk_node(pairs[0])
    q = [root]

    i = 1
    for node in q:
        if not node.is_leaf:
            node.top_left = mk_node(pairs[i])
            node.top_right = mk_node(pairs[i+1])
            node.bottom_left = mk_node(pairs[i+2])
            node.bottom_right = mk_node(pairs[i+3])

            q.extend([node.top_left, node.top_right, node.bottom_left, node.bottom_right])
            i += 4

    return root

class GraphNode:
    def __init__(self, val: int = 0, neighbors: list[GraphNode] | None = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def _encode_graph(self) -> str:
        nodes = {self.val: self}
        q = [self]

        for node in q:
            for nei in node.neighbors:
                if nei.val not in nodes:
                    nodes[nei.val] = nei
                    q.append(nei)

        res = []
        for val in sorted(nodes):
            res.append(f"[{','.join(str(nei.val) for nei in nodes[val].neighbors)}]")

        return f"G[{','.join(res)}]"

    def __str__(self):
        return self._encode_graph()

def _decode_graph(input: str):
    if input == "G[]":
        return None

    adj_raw = input[3:-2].split("],[")
    adj = [
        [int(x) for x in neis.split(',')] if neis
        else []
        for neis in adj_raw
    ]

    nodes = [GraphNode(i) for i in range(len(adj))]

    for i, neis in enumerate(adj):
        nodes[i].neighbors = [nodes[val] for val in neis]

    return nodes[0]

class Interval:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __str__(self):
        return f"[{self.start},{self.end}]"

def _encode_intervals(input: list[Interval]) -> str:
    res = []
    for interval in input:
        res.append(str(interval))
    return f"I[{','.join(res)}]"

def _decode_intervals(input: str) -> list[Interval]:
    if input == "I[]":
        return []

    intervals = input[3:-2].split("],[")
    res = []

    for interval in intervals:
        start, end = interval.split(',')
        res.append(Interval(int(start), int(end)))

    return res

class MountainArray:
    def __init__(self, arr: list[int]):
        self.arr = arr

    def get(self, index: int) -> int:
        return self.arr[index]

    def length(self) -> int:
        return len(self.arr)

def api_guess_number_higher_or_lower(pick: int):
    def guess(num: int) -> int:
        if num < pick:
            return 1
        elif num > pick:
            return -1
        return 0
    return guess

def _encode_type(x: Any) -> str:
    if isinstance(x, list):
        if x and isinstance(x[0], Interval):
            return _encode_intervals(x)
        return str(x).replace(', ', ',')
    elif isinstance(x, dict):
        return str(x).replace(', ', ',').replace(': ', ':')
    return str(x)

def _decode_type(x: str) -> Any:
    if x.startswith("L["):
        return _decode_linked_list(x)
    elif x.startswith("T["):
        return _decode_binary_tree(x)
    elif x.startswith("Q["):
        return _decode_quad_tree(x)
    elif x.startswith("G["):
        return _decode_graph(x)
    elif x.startswith("I["):
        return _decode_intervals(x)
    return x
