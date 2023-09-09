from typing import List
from functions import Function, Parameter

class LoadFile(Function):

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Enter a file name"

    def execute(self, input: str) -> str:
        f = open(f"{input}", "r")

        f.close()
        return ""

