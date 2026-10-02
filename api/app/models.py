from pydantic import BaseModel


class SubmitRequest(BaseModel):
    problem_slug: str
    code: str


class RunRequest(BaseModel):
    problem_slug: str
    code: str
    custom_tests: list[str]
