import re
import sys
import json
import textwrap
from typing import Any
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.data_structures import _encode_type, _decode_type

PROBLEMS_PATH = Path(__file__).resolve().parents[3] / "shared" / "problems.json"
SOLUTIONS_PATH = Path(__file__).resolve().parents[2] / "solutions.json"

# parses constraints like `1 <= nums.length <= 10^5` to identify min/max constants
PATTERN = re.compile(r"""
    ^\s*
    `?
    ([-\d\s*^]+)
    \s*<=\s*
    ([a-zA-Z0-9_., \[\]]+?)
    \s*<=\s*
    ([-\d\s*^]+)
    `?
    \s*$
""", re.VERBOSE)

def _clean_name(var: str) -> str:
    var = re.sub(r"\.(length|size)", "_len", var.strip())
    var = re.sub(r"\[.*?\]", "_val", var)
    return var.upper()

def _eval_num(expr: str) -> int:
    return int(eval(expr.replace("^", "**")))

def get_constraints(problem_slug: str) -> SimpleNamespace:
    with open(PROBLEMS_PATH) as f:
        problem = json.load(f)[problem_slug]

    consts = {}
    for c in problem["constraints"]:
        match = PATTERN.match(c)
        # skip if constraint is not of standard `1 <= nums.length <= 10^5` form
        if not match:
            continue
        lo_str, vars, hi_str = match.groups()
        lo, hi = _eval_num(lo_str), _eval_num(hi_str)

        for var in vars.split(", "):
            base = _clean_name(var)
            consts[f"{base}_MIN"] = lo
            consts[f"{base}_MAX"] = hi

    return SimpleNamespace(**consts)

def _to_pascal_case(name: str) -> str:
    words = re.findall(r"[a-zA-Z0-9]+", name)
    return "".join(w.capitalize() for w in words)

def _to_snake_case(name: str) -> str:
    words = re.findall(r"[a-zA-Z0-9]+", name)
    return '_'.join(w.lower() for w in words)

def _parse_solution(problem_slug: str) -> str:
    with open(PROBLEMS_PATH) as f:
        problems = json.load(f)
    with open(SOLUTIONS_PATH) as f:
        solutions = json.load(f)

    name = problems[problem_slug]["name"]
    prob_code = problems[problem_slug]["code"]
    sol_code = solutions[problem_slug]

    # problems["code"] started with `def ` signifies class problem, since those show methods
    if prob_code.startswith("def "):
        class_name = _to_pascal_case(name)
        sol_indented = textwrap.indent(sol_code, "\t")
        return f"class {class_name}:\n{sol_indented}"

    fn_name = _to_snake_case(name)
    paren_l = prob_code.find("(")
    paren_r = prob_code.find(")")
    args = prob_code[paren_l+1 : paren_r]
    return_type = prob_code[paren_r+1:]

    method_header = (
        f"def {fn_name}(self, {args})" if args
        else f"def {fn_name}(self)"
    ) + f"{return_type}:"

    return f"class Solution:\n\t{method_header}\n{textwrap.indent(sol_code, '\t\t')}"

def get_expected_outputs(problem_slug: str, inputs: list):
    namespace = {}
    exec(_parse_solution(problem_slug), namespace)

    with open(PROBLEMS_PATH) as f:
        problem = json.load(f)[problem_slug]

    name = problem["name"]
    is_class = problem["code"].startswith("def ")

    if not is_class:
        solver = getattr(namespace["Solution"](), _to_snake_case(name))
        # unpack if multiple args wrapped in a tuple, else just supply the 1 arg
        return [
            solver(*item) if isinstance(item, tuple)
            else solver(item)
            for item in inputs
        ]

    cls = namespace[_to_pascal_case(name)]
    outputs = []

    for test in inputs:
        # test is a list of calls: [("__init__", [args]), ("method", [args]), ...]
        init_call, *method_calls = test
        obj = cls(*init_call[1])
        res = [None]
        for method, args in method_calls:
            args_decoded = [_decode_type(arg) for arg in args]
            res.append(getattr(obj, method)(*args_decoded))
        outputs.append(res)
    return outputs

def write_hidden_tests(problem_slug: str, inputs: list, outputs: list) -> None:
    blocks = []

    for inp, out in zip(inputs, outputs):
        args = [*inp, out] if isinstance(inp, tuple) else [inp, out]
        lines = [_encode_type(arg) for arg in args]
        blocks.append("\n".join(lines))

    f = Path(__file__).resolve().parents[1] / "hidden" / f"{problem_slug}.txt"
    f.write_text("\n\n".join(blocks) + "\n")
