import os
import requests
from langchain_anthropic import ChatAnthropic

# defining api keys
os.environ["ANTHROPIC_API_KEY"] = "<ENTER YOUR API KEY>"

# initializing llm model
llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=1)

# function to get weather information using the Tomorrow.io API
def get_info(input: str):
    
    # json data for the current weather
    url = "https://api.tomorrow.io/v4/weather/realtime"
    param = {
        "apikey": "<ENTER YOUR API KEY>",
        "location": input,
        "units": "imperial",
    }
    current = requests.get(url, params=param).json()
    if "message" in current:
        return f"Error: {current['message']}"

    # json data for the weather forecast
    base_url = "https://api.tomorrow.io/v4/timelines"
    params = {
        "apikey": "<ENTER YOUR API KEY>",
        "location": input,
        "fields": ["temperature", "temperatureMax", "temperatureMin", "precipitationProbability"],
        "timesteps": "1d",
        "units": "imperial",
        "timezone": "America/Los_Angeles"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if "message" in data:
        return f"Error: {data['message']}"
    
    # getting the current weather attributes
    cur_temp = current['data']['values']['temperature']
    rain = current['data']['values']['precipitationProbability']
    wind = current['data']['values']['windSpeed']
    humid = current['data']['values']['humidity']

    # getting the 7 day weather forecast high and low temperatures
    forecasts = data['data']['timelines'][0]['intervals']
    f_info = []
    for f in forecasts:
        day = f['startTime'][:10]  # Extract the date
        min = f['values']['temperatureMin']
        max = f['values']['temperatureMax']
        f_info.append(f"{day}:  Low {min:.2f} °F,   High {max:.2f} °F")

    forecast = "\n".join(f_info)
    cur_weather = f"Temperature: {cur_temp} °F\nPrecipitation: {rain} %\nWind Speed: {wind} mph\nHumidity: {humid} %\n"

    return [cur_weather, forecast]


def ai_assist(query: str):
    # initializing the ai assistant to offer help and details on the weather
    prompt = f"You are a virtual weather assistant. Provide a short paragraph response on clothing, and weather information based on the following query: {query}"
    response = llm(prompt)
    return response


def clean(response):
    # removing filler characters from the metadata to provide a clean user response
    lines = response.content.splitlines()
    cleaned = []

    # iterating through the lines and clean each one
    for line in lines:
        if line.strip():  # only append if the line isn't empty
            cleaned.append(f"{line.strip()}")
            
    return "\n".join(cleaned)
