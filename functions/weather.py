from typing import List
from functions import Function, Parameter
import requests

class WeatherSearch(Function):
    def __init__(self) -> None:
        self.baseUrl = "https://api.openweathermap.org/data/3.0/onecall?"
        self.api_key = "d8fc034210ecf319559513eccde4fd87"


    @property
    def name(self) -> str:
        return "weather_search"

    @property
    def description(self) -> str:
        return "Enter latitude and longitude. Returns temperature in Kelvin."

    @property
    def parameters(self) -> List[Parameter]:
         return super().parameters

    def execute(self, input: str) -> str:
        print(f"This is input: {input}")
        parameters = input.split(", ")
        print(f"This is parameters[0]: {parameters[0]}")
        print(f"This is parameters[1]: {parameters[1]}")
        url = self.baseUrl + f"lat={parameters[0]}" + f"&lon={parameters[1]}" + f"&appid={self.api_key}"
        response = requests.get(url).json()
        # print(response)
        t = response['current']['temp']
        return f"{t} Kevin"


