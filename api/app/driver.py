import io
import contextlib
import time
import tracemalloc
import signal
import resource
from typing import Any, Callable

from app.data_structures import (
    LinkedListNode,
    BinaryTreeNode,
    QuadTreeNode,
    GraphNode,
    Interval,
    MountainArray,
    api_guess_number_higher_or_lower,
    _decode_type,
)


def _timeout_handler(signum, frame):
    raise TimeoutError("Time Limit Exceeded")


def set_limits(time_ms: int, space_mb: int) -> float:
    bytes_limit = space_mb * 2**20
    resource.setrlimit(resource.RLIMIT_AS, (bytes_limit, bytes_limit))
    return time_ms / 1000.0


def run_with_limits(
    fn: Callable, args: tuple, time_sec: float, space_bytes: int
) -> tuple[Any, str, float, int]:
    stdout_buf = io.StringIO()
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.setitimer(signal.ITIMER_REAL, time_sec)
    tracemalloc.start()
    start = time.perf_counter()

    try:
        with contextlib.redirect_stdout(stdout_buf):
            res = fn(*args)
    finally:
        elapsed = time.perf_counter() - start
        signal.setitimer(signal.ITIMER_REAL, 0)
        _, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    if peak_bytes > space_bytes:
        limit_mb = space_bytes / 2**20
        peak_mb = peak_bytes / 2**20
        raise MemoryError(
            f"Memory Limit Exceeded: used {peak_mb:.2f} MB, limit is {limit_mb:.2f} MB"
        )

    return res, stdout_buf.getvalue(), elapsed, peak_bytes


"""
try:
    ...
except TimeoutError:
    # Time Limit Exceeded
except MemoryError:
    # Memory Limit Exceeded
except Exception as e:
    # Runtime Error
"""
