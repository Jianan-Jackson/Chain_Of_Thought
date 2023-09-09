from typing import List
from .function import Parameter
from .function import Function
import os
import json
import requests

class News(Function):
    @property
    def name(self) -> str:
        return 'get_news'

    @property
    def description(self) -> str:
        return 'Takes query as input to search for news aritcles in json format as ```{"query": "blockchain"}```. Returns the top 10 articles about the query provided. It returns an empty array if no articles are found'

    @property
    def parameters(self) -> List[Parameter]:
        return [
            Parameter(
                name="query",
                param_type="string",
                description="Query you want make to the news API.",
                required=True,
            ),
        ]

    def execute(self, input: str) -> str:
        json_data = json.loads(input)
        url = ('https://newsapi.org/v2/everything?' +
            'q={}&'.format(json_data['query']) +
            'from=2023-06-16&' +
            'sortBy=popularity&' +
            'apiKey={key}').format(key=os.environ.get('NEWSAPI_API_KEY'))
        response = requests.get(url)
        articles = [{"title": item["title"], "description": item["description"], "image": item["urlToImage"], "news_url": item["url"]} for item in response.json()['articles'][:10]]
        return articles