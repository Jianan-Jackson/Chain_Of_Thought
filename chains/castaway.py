from .chain import Chain
from indices import FunctionIndex
import openai
from utils import Logger

import datetime
import logging

import json


class Castaway(Chain):
    _SYSTEM_MESSAGE = """Current datetime: <DATETIME>. Complete the user's request."""

    _index: FunctionIndex

    def __init__(self, index: FunctionIndex, logger: Logger):
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self._SYSTEM_MESSAGE = self._SYSTEM_MESSAGE.replace(
            "<DATETIME>", current_datetime
        )
        self._messages = []
        self._relevant_functions = {}

        self._index = index
        self._logger = logger

    def run(self, query: str, max_steps: int = 20):
        self._messages = [
            {"role": "system", "content": self._SYSTEM_MESSAGE},
            {"role": "user", "content": "What is Joe rogan's age raised to the power of 0.23?"},
            {"role": "assistant", "content": "I now know Joe Rogan is 55 years old as of right now. I need to raise that to the power of 0.23."}
        ]

        self._relevant_functions = {function.name : function for function in self._index.retrieve(query)}
        response = openai.ChatCompletion.create(
            model='gpt-4-0613',
            temperature=0,
            messages=self._messages,
            functions=[action.to_dict() for action in self._actions.values()],
        )

        function_name = response.choices[0]['message']['function_call']['name']
        function_args = response.choices[0]['message']['function_call']['arguments']
        function_args = json.loads(function_args)
        function_result = self._relevant_functions[function_name].execute(**function_args)


        return response


    def _generate_next_thought(self, previous_thought: str) -> str:
        pass
