import sys
import os
sys.path.insert(0, os.path.dirname(os.getcwd()))

from nlp.InfoExtraction import get_chunks
import pyowm


def bot_agent(text):
    if keywordDetection(text):
        print('### WEATHER KEYWORD DETECTED ###')
        ## get_entities
        if GPE_detection(text):
            # if GPE Found
            # call weather api provider
            ## get gpe entity chunk
            ## respond
            city = get_chunks(text, 'GPE')[0]
            ### GPE DETECTED ###
            print('### GPE DETECTED ###')
            return bot_response(city)
        elif coordinate_detection(text):
            ## respond
            pass
    else:
        ## the sentence can't be parsed
        ## does not contain the information relative to the weather
        return bot_response()


def keywordDetection(text):
    keyword = 'weather'
    if keyword in text.lower():
        return True
    return False


def coordinate_detection(text):
    pass


def GPE_detection(text):
    return True if len(get_chunks(text, 'GPE'))>0 else False


def bot_response(city=None):
    try:
        if city is not None:
            weather = weather_agent(city)
            temp = weather.get_temp()
            response = "Temperature in " + city + " is " + str(temp)
            return response
        else:
            response = "I can't understand your sentence structure !!"
            return response
    except Exception:
        response = "Sorry, I can't reach out this city !"
        return response


### WEATHER API PROVIDER ###
class weather_agent:
    
    def __init__(self, gpe, cord=None):
        self.__api_key = '8e4495c794168a84daa4a6144dada881'
        self.__owm = pyowm.OWM(self.__api_key)  
        self.__observation = self.__owm.weather_at_place(gpe)
        self.__w = self.__observation.get_weather()
        self.__wind = self.__w.get_wind()                  # {'speed': 4.6, 'deg': 330}
        self.__humidity = self.__w.get_humidity()          # 87
        self.__temp = self.__w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
        self.__city = gpe
        
        if cord is not None:
            # Search current weather observations in the surroundings of
            # lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
            observation_list = self.__owm.weather_around_coords(cord[0], cord[1])
        

    def get_humidity(self):
        return self.__humidity

    def get_max_temp(self):
        return self.__temp['temp_max']

    def get_min_temp(self):
        return self.__temp['temp_min']

    def get_temp(self):
        return self.__temp['temp']

    def get_wind_speed(self):
        return self.__wind

    def get_city(self):
        return self.__city


# print(get_chunks('What is weather like in London', 'GPE'))
# print(GPE_detection('What is weather like in London'))
# print(bot_agent("What is weather like in London"))
# print(bot_agent('How old are you'))