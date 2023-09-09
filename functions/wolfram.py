from .function import Function
import wolframalpha

class WolframAlpha(Function):

    client: wolframalpha.Client

    def __init__(self) -> None:
        self.client = wolframalpha.Client('2E6E47-KJTK7VE42U')

    @property
    def name(self) -> str:
        return 'Wolfram Alpha'

    @property
    def description(self) -> str:
        return '''Access dynamic computation and curated data from Wolfram Alpha. Enter math expressions such as '(12*0.1)^2/sin(pi/2)' as action input to evaluate.'''

    def execute(self, input: str) -> str:
        response = self.client.query(input)
        result = ''  
        for pod in response.pods:
            if pod is not None and pod.text is not None:
                result += pod.text + '\n'
        return result