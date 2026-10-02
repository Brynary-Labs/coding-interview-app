import sys
import json
import asyncio
from fastapi import FastAPI
from app.models import SubmitRequest, RunRequest

app = FastAPI()


@app.post("/submit")
async def submit_code(req: SubmitRequest):
    args = [sys.executable, "-m", "app.driver", req.problem_slug, "--mode", "submit"]

    proc = await asyncio.create_subprocess_exec(
        *args,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate(req.code.encode())
    return json.loads(stdout.decode())


@app.post("/run")
async def run_code(req: RunRequest):
    args = [sys.executable, "-m", "app.driver", req.problem_slug, "--mode", "run"]

    if req.custom_tests:
        args.extend(["--custom", req.custom_tests])

    proc = await asyncio.create_subprocess_exec(
        *args,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate(req.code.encode())
    return json.loads(stdout.decode())
