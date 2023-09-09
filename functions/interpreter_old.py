import sys
import io

from typing import List
from functions import Function, Parameter

class InterpreterOld(Function):
    @property
    def name(self) -> str:
        return 'python_interpreter'
    
    @property
    def description(self) -> str:
        return 'Write Python code and run it through this function. You must use print() statement for there to be any output.'
    
    @property
    def parameters(self) -> List[Parameter]:
        return [
            Parameter(
                name="code",
                param_type="string",
                description="Code you would like to execute. You must use print() statement for there to be any output.",
                required=True,
            )
        ]
    
    def execute(self, code: str) -> str:
        # Create a new output stream
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()

        # Try to execute the code
        try:
            exec(code)
        except Exception as e:
            print("An error occurred: ", e)
        finally:
            # Reset the standard output
            sys.stdout = old_stdout

        # Get the output and return it
        response = redirected_output.getvalue()
        if response.endswith('\n'):
            response = response[:-1]
        return response
