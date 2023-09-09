from typing import List
from .function import Parameter
from .function import Function
from utils.openai_utils import get_turbo_response, get_gpt4_response

class ReadStory(Function):

    ''' read history from story.txt '''

    @property
    def name(self) -> str:
        return 'read_story'

    @property
    def description(self) -> str:
        return "Ask a question you want to know the user, based on past interactions with the system. You can use this function to get insights on user's preference, requests, etc. Returns text answer." 

    @property
    def parameters(self) -> List[Parameter]:
         return super().parameters

    def execute(self, query: str) -> str:
        
        with open('story.txt', 'r') as f:
            story = f.read()

        msg = [
            {'role': 'system', 'content': "Given the history of past interactions, answer the query. Your answer must be based on the materials provided."},
            {'role': 'system', 'content': f"{story}\n----\nQUERY: {query}"}
        ]
        response = get_gpt4_response(msg, max_tokens=256)

        return response['content']