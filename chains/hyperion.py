from .chain import Chain
from indices import FunctionIndex

from utils import get_gpt4_response, get_turbo_response
from utils import Logger

import datetime
import re
import logging

import json

class Hyperion(Chain):

    _SYSTEM_MESSAGE = '''Current datetime: {datetime}. You will solve the user's task by choosing right step to take. Your response must always be picked from the listed formats with swapped out curly brackets for values. Here's a log of you, the assistant, interacting the the user in the past:\n{story}'''

    # Transition pieces
    _NON_FUNCTION_TRANSITION = '''----\nPick one of the following responses:\n- THOUGHT: {your thoughts on what to do next. Need to be simple and fit into one sentence}<END>\n- CONCLUSION: {a conclusion when you believe the current task is done. This piece of text could be final answer or follow up questions.}<END>\n----'''
    _FUNCTION_TRANSITION = '''----\nPick one of the following responses:\n- THOUGHT: {your thoughts on what to do next. Need to be simple and fit into one sentence}<END>\n- FUNCTION: {name of the function you pick}, INPUT: {input to this function}<END>\n- CONCLUSION: {a conclusion when you believe the current task is complete, cannot be done, or requires further information. This piece of text could be final answer or follow up questions.}<END>\nIf you pick FUNCTION, you must pick from the following list:\n<FUNCTIONS>\n----'''

    # Regexes
    _THOUGHT_REGEX = r"\s*THOUGHT:\s*(.*)"
    _FUNCTION_REGEX = r"\s*FUNCTION:\s*(.*?)\s*,\s*INPUT:(.*)"
    _CONCLUSION_REGEX = r"\s*CONCLUSION:\s*(.*)"

    _index: FunctionIndex

    def __init__(self, index: FunctionIndex, logger: Logger):
        
        
        
        # self._SYSTEM_MESSAGE = self._SYSTEM_MESSAGE.replace('<DATETIME>', current_datetime)
        self._messages = []

        self._index = index
        self._logger = logger


    def run(self, query: str, max_steps: int = 20):

        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with open('story.txt', 'r') as f:
            story = f.read()

        self._SYSTEM_MESSAGE = self._SYSTEM_MESSAGE.format(
            datetime=current_datetime,
            story=story
        )
        self._messages = [{'role': 'system', 'content': self._SYSTEM_MESSAGE}]

        self._add_user_message(query)
        self._add_user_message(self._NON_FUNCTION_TRANSITION)

        conclusion_reached: bool = False
        generated_wrong_format: bool = False
        current_step: int = 0

        while (
            current_step < max_steps 
            and not conclusion_reached
            and not generated_wrong_format
        ):
            response = get_gpt4_response(self._messages)['content']
            # print(f"This is GPT response: {response}")
            # self._logger.log(response, category='INFO')
            if 'THOUGHT' in response:
                self._handle_thought(response)
            elif 'FUNCTION' in response:
                self._handle_function(response)
            elif 'CONCLUSION' in response:
                self._handle_conclusion(response)
                conclusion_reached = True
            else:
                # Hallucination
                self._logger.log(response, category='HALLUCINATION')
                generated_wrong_format = True
            current_step += 1
    
    def _handle_thought(self, response: str):
        thought = re.search(self._THOUGHT_REGEX, response).group(1)
        self._logger.log(thought, category='THOUGHT')
        self._add_assistant_message(f'THOUGHT: {thought}<END>')
        self._remove_transition_piece()
        functions = self._index.retrieve(thought, k=10)

        function_list = '\n'.join([f'- {function.name}: {function.description}' for function in functions])
        self._add_user_message(self._FUNCTION_TRANSITION.replace('<FUNCTIONS>', function_list))
    
    def _handle_function(self, response: str):
        function_match = re.search(self._FUNCTION_REGEX, response, re.DOTALL)
        function_name = function_match.group(1).strip()
        function_input = function_match.group(2).strip()

        self._logger.log(f'\n{function_name}', category='FUNCTION')
        self._logger.log(f'\n{function_input}', category='INPUT')

        self._add_assistant_message(f'FUNCTION: {function_name}, INPUT: {function_input}<END>')
        self._remove_transition_piece()
        if self._index.get(function_name) is None:
            self._add_user_message('Error: invalid function name. Choose from the listed ones only.')
        else:
            function_response = self._index.get(function_name).execute(function_input)
            function_response = function_response.replace('\n\n', '\n')
            self._logger.log(f'\n{function_response}\n', category='RESPONSE')
            self._add_user_message(f'RESPONSE: {function_response}')
            self._add_user_message(self._NON_FUNCTION_TRANSITION)

                


    def _handle_conclusion(self, response: str):
        conclusion = re.search(self._CONCLUSION_REGEX, response).group(1)
        self._remove_transition_piece()
        self._logger.log(conclusion, category='CONCLUSION')
        self._add_assistant_message(f'CONCLUSION: {conclusion}<END>')
        self._write_story()

    
    def _write_story(self):
        with open('story.txt', 'a') as f:  # 'a' for appending instead of 'w' for overwriting
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            f.write(f'Current datetime: {current_datetime}\n')
            # assuming `response` contains the story to be written
            f.write(str(self._messages) + '\n\n')
            



    def _add_user_message(self, message: str):
        self._messages.append({'role': 'user', 'content': message})


    def _add_assistant_message(self, message: str):
        self._messages.append({'role': 'assistant', 'content': message})


    def _remove_transition_piece(self):
        index = 0
        while index < len(self._messages):
            role = self._messages[index]['role']
            content = self._messages[index]['content']
            if (role == 'user' and
                content.startswith('----') and
                content.endswith('----')):
                self._messages.pop(index)
            index += 1