from .function import Function
from langchain.utilities import WikipediaAPIWrapper

from utils.openai_utils import get_turbo_response


class WikipediaSearch(Function):

    search: WikipediaAPIWrapper
    
    def __init__(self) -> None:
        self.search = WikipediaAPIWrapper()
    
    @property
    def name(self) -> str:
        return 'Wikipedia Search'

    @property
    def description(self) -> str:
        return 'Enter keywords, returns answer from relevant Wikipedia articles.'
    
    def execute(self, input: str) -> str:
        result = self.search.run(input)
        msg = [
            {'role': 'system', 'content': "Answer the user's query based on materials presented. Respond as concise as possible. If the given material does not explicitly provide information about user's query, admit so."},
            {'role': 'system', 'content': f"{result}\n----\nQUERY: {input}"}
        ]
        response = get_turbo_response(msg)
        return response['content']