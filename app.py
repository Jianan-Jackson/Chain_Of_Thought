import os
import platform
import openai
import config

import chains
import indices

from functions import GoogleSearch
from functions import WolframAlpha
from functions import InterpreterOld
from functions import WeatherSearch
from functions import Mail
from functions import News

from utils import TerminalLogger

def main():
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    tmd = TerminalLogger()
    tmd.set_color('THOUGHT', 'purple')
    tmd.set_color('RELEVANT', 'cyan')
    tmd.set_color('FUNCTION', 'green')
    tmd.set_color('INPUT', 'green')
    tmd.set_color('RESPONSE', 'green')
    tmd.set_color('CONCLUSION', 'yellow')
    tmd.set_color('HALLUCINATION', 'red')

    index = indices.IntentIndex(tmd)
    index.put(GoogleSearch())
    index.put(InterpreterOld())
    index.put(WeatherSearch())
    index.put(Mail())
    index.put(News())
    # index.put(ReadStory())

    chain = chains.Hyperion(index, tmd)

    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

    while True:
        query = input('> ')
        if query.lower() == 'exit':
            break
        else:
            print()
            chain.run(query)

if __name__ == '__main__':
    main()