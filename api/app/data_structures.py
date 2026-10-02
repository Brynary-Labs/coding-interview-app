from typing import Any

class LinkedListNode:
    def __init__(
        self,
        val: Any = 0,
        next: Any = None,
        prev: Any = None,
        key: Any = None,
        random: LinkedListNode | None = None,
        cycle: LinkedListNode | None = None
    ):
        self.val = val
        self.next = next
        self.prev = prev
        self.key = key
        self.random = random
        self.cycle = cycle

    def __str__(self):
        ll_traversed = []
        curr = self
        while curr:
            ll_traversed.append(curr.val)
            curr = curr.next
        return f"L[{','.join(ll_traversed)}]"

def _decode_linked_list(input: str) -> LinkedListNode:
    vals = input[2:-1].split(',')
    dummy = curr = LinkedListNode()
    for i in range(len(vals)):
        curr.next = LinkedListNode(vals[i])
        curr = curr.next
    return dummy.next

class Interval:
    def __init__(self, start: Any, end: Any):
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
    intervals = input[2:-1].split("],[")
    res = []
    for start, end in intervals:
        res.append(Interval(start, end))
    return res

def _encode_type(x: Any) -> str:
    if isinstance(x, list):
        return str(x).replace(', ', ',')
    elif isinstance(x, dict):
        return str(x).replace(', ', ',').replace(': ', ':')
    elif isinstance(x, list[Interval]):
        return _encode_intervals(x)
    return str(x)

def _decode_type(x: str) -> Any:
    if x.startswith("L["):
        _decode_linked_list(x)
    # elif x.startswith("T["):
    #     _decode_binary_tree(x)
    # elif x.startswith("Q["):
    #     _decode_quad_tree(x)
    # elif x.startswith("G["):
    #     _decode_graph(x)
    elif x.startswith("I["):
        _decode_intervals(x)
    return x
