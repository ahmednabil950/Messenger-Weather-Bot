import sys
import os
sys.path.insert(0, os.path.dirname(os.getcwd()))

from nlp.InfoExtraction import get_chunks
import pyowm
import string


def bot_text_agent(text):
    if GPE_detection(text):
        # if GPE Found
        # call weather api provider
        ## get gpe entity chunk
        ## respond
        city = get_chunks(text, 'GPE')[0]
        ### GPE DETECTED ###
        print('### GPE DETECTED ###')
        return weather_response(city)
    elif small_talk_detection(text) is not None:
        idx = small_talk_detection(text)
        return small_talk_answer(idx)
    else:
        ## the sentence can't be parsed
        ## does not contain the information relative to the weather
        return respond_to("CANT_UNDERSTAND")

def bot_btns_agent(text, cord=None):
    if keyword_detection(text, "Via City"):
        return respond_to("VIA_CITY")
    elif keyword_detection(text, "Via GPS"):
        return weather_response(cord=cord)
    elif keyword_detection(text, "Main Menu"):
        return respond_to("GET_STARTED")

def keyword_detection(text, keyword):
    keyword = keyword.lower()
    if keyword in text.lower():
        return True
    return False

def coordinate_detection(text):
    pass

def GPE_detection(text):
    return True if len(get_chunks(text, 'GPE'))>0 else False

def weather_response(city=None, cord=None):
    try:
        if city is not None:
            weather = weather_agent(city)
            return retrieve_responses(weather, respond_to("WEATHER"))
        elif cord is not None:
            weather = weather_agent(cord=cord)
            return retrieve_responses(weather, respond_to("WEATHER"))
    except Exception:
        response = respond_to("NOT_FOUND")
        return response

def respond_to(key=None):
    respond = {
        "FACEBOOK_WELCOME": ['Greetings !, I am a weather robot glad to help you to find the forecast'],
        "NOT_FOUND": ["Sorry, I can't reach out this city !"],
        "GET_STARTED": ["How would you like to get a weather forecast?"],
        "TEMP": ["Temperature in <city> is <value> Celsius"],
        "WEATHER": {
            "TITLE": "Here is the forecast i found",
            "TEMP": "Temperature is <value> Celsius",
            "MAX": "Maximum temperature is <value> Celssius",
            "MIN": "Minimum temperature is <value> Celssius",
            "HUMIDITY": "Humidity is <value> %",
            "STATUS": "Weather status <value>",
            "WIND": "Wind speed is <value> m/s",
        },
        "CANT_UNDERSTAND": ["I can't understand your sentence structure !!"],
        "VIA_CITY": ["Please enter the city name"],
        "VIA_GPS": ["Please wait i am getting your GPS coordinates",
            {
                "WEATHER": {
                "TITLE": "Here is the forecast i found",
                "TEMP": "Temperature is <value> Celsius",
                "MAX": "Maximum temperature is <value> Celssius",
                "MIN": "Minimum temperature is <value> Celssius",
                "HUMIDITY": "Humidity is <value> %",
                "STATUS": "Weather status <value>",
                "WIND": "Wind speed is <value> m/s",
            }
        }]
    }
    return respond[key] if key is not None else respond

def small_talk():
    return [
        {
            'QUESTION': "Are you there?",
            'ANSWER': ["I am Here to help you"], respond_to('GET_STARTED')
        },
        {
            'QUESTION': "How old are you?",
            'ANSWER': ["I have been developed recently for the purpose of weather forecast"]
        },
        {
            'QUESTION': "You are beautiful",
            'ANSWER': ["Thanks, at your service always"]
        },
        {
            'QUESTION': "You are a chatbot",
            'ANSWER': ["Yes, Ask me about the weather via location or city name and i will be glad to find it"]
        },
        {
            'QUESTION': "Are you ready?",
            'ANSWER': ["Yes, Just give me your location or city name"]
        },
        {
            'QUESTION': "You're so clever.",
            'ANSWER': ["You are welcome, Glad to hear it"]
        }
    ]

def small_talk_detection(text):
    talks = small_talk()
    text = remove_punctuation(text)
    for idx, talk in enumerate(talks):
        if text.lower() in talk['QUESTION'].lower():
            return idx

def small_talk_answer(idx):
    return small_talk()[idx]['ANSWER']

def retrieve_responses(weather_provider, responses):
    all_resp = []
    temp = str(weather_provider.get_temp())
    humidity = str(weather_provider.get_humidity())
    wind = str(weather_provider.get_wind_speed())
    max_temp = str(weather_provider.get_max_temp())
    min_temp = str(weather_provider.get_min_temp())
    status = str(weather_provider.get_status())
    
    all_resp.append(responses["TITLE"])
    all_resp.append(responses["TEMP"].replace("<value>", temp))
    all_resp.append(responses["MAX"].replace("<value>", max_temp))
    all_resp.append(responses["MIN"].replace("<value>", min_temp))
    all_resp.append(responses["STATUS"].replace("<value>", status))
    all_resp.append(responses["HUMIDITY"].replace("<value>", humidity))
    all_resp.append(responses["WIND"].replace("<value>", wind))
    return all_resp

def remove_punctuation(s):
    return s.translate(str.maketrans('','',string.punctuation))

### WEATHER API PROVIDER ###
class weather_agent:
    
    def __init__(self, gpe= None, cord=None):
        self.__api_key = '8e4495c794168a84daa4a6144dada881'
        self.__owm = pyowm.OWM(self.__api_key)
        if cord is None:
            # search using city name
            self.__observation = self.__owm.weather_at_place(gpe)
        elif gpe is None:
            # Search current weather observations in the surroundings of
            # lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
            obser_lst = self.__owm.weather_around_coords(cord[0], cord[1])
            self.__observation = obser_lst[0]
        self.__w = self.__observation.get_weather()
        self.__city = gpe
                

    def get_humidity(self):
        return self.__w.get_humidity()

    def get_max_temp(self):
        temp_max = self.__w.get_temperature('celsius')
        return temp_max['temp_max']

    def get_min_temp(self):
        temp_min = self.__w.get_temperature('celsius')
        return temp_min['temp_min']

    def get_temp(self):
        temp = self.__w.get_temperature('celsius')
        return temp['temp']

    def get_wind_speed(self):
        return self.__w.get_wind()["speed"]

    def get_city(self):
        return self.__city

    def get_status(self):
        return self.__w.get_status()


# print(get_chunks('What is weather like in London', 'GPE'))
# print(GPE_detection('What is weather like in London'))
# print(bot_text_agent("What is weather like in London"))
# print(bot_text_agent('How old are you'))
# print(bot_text_agent("Are you there?"))
# print(small_talk()[1]['QUESTION'])
# print(small_talk_detection("Are you there?"))
# print(small_talk_detection("are you there?"))
# print(remove_punctuation("Are you there?"))