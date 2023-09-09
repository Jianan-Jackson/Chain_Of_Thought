import sys
import io

from typing import List
from functions import Function, Parameter

class Interpreter(Function):
    @property
    def name(self) -> str:
        return 'python_interpreter'
    
    @property
    def description(self) -> str:
        return 'Write Python code and run it through this function'
    
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


    def execute(self, **kwargs) -> str:
        code = kwargs['code']

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
        return redirected_output.getvalue()
