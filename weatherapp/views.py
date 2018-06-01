from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from utils.messenger import messenger
from bot.bot import bot_text_agent
from bot.bot import bot_btns_agent
from bot.bot import weather_response
from bot.bot import respond_to
from django.views.decorators.csrf import csrf_exempt
import requests
import json


@csrf_exempt
def main_view(request):
    if request.method == 'GET':
        return bot_access_token(request)

    if request.method == 'POST':
        return bot_sender(request)


def bot_access_token(request):
    bot = messenger()

    if request.method == 'GET':
        token_sent = request.GET.get("hub.verify_token")
        if bot.Verify_Token(token_sent):
            return HttpResponse(request.GET.get("hub.challenge"))
    return HttpResponse()


@csrf_exempt
def bot_sender(request):

    print(request)

    bot = messenger()

    ###### Here the Main Menu #####
    ####################################################
    ## code here !!

    if request.method == 'POST':
        
        print("###### JSON FORMAT ######")
        all_json = json.loads(request.body.decode('utf-8'))
        recipient_id = bot.get_receptient_ID(all_json)
        print(all_json)
        
        print("###### JSON STATUS ######")
        json_status = bot.check_json_sent(all_json)
        print(json_status)

        ###### Here the input is text from the chatbot #####
        ####################################################
        if json_status == "text":
            try:
                text = bot.get_received_text(all_json)
                text = str(text)
                response = bot_text_agent(text)
                ############ LOGS ##################################
                print("####### TEXT DATATYPE #######")
                print(type(text))
                print("####### TXT IS #######")
                print(text)
                print("####### RSP IS #######")
                print(response)
                ####################################################
                bot.send_text_msgs(response, "RESPONSE", recipient_id)
                if response == respond_to("CANT_UNDERSTAND"):
                    ### If the user entered invalid text ###
                    ### Show Menu Button !! ###
                    bot.main_menu(recipient_id)
            except requests.exceptions.Timeout:
                print("time out")
        elif json_status == "postback":
            ###### Here the input is get started button #####
            ####################################################
            postback = bot.get_postback(all_json)
            if postback.get('payload'):
                response = respond_to("FACEBOOK_WELCOME")
                bot.send_text_msgs(response, "RESPONSE", recipient_id)
                get_started_msg = respond_to("GET_STARTED")[0]
            bot.quick_reply(get_started_msg, quick_reply_btns(), recipient_id)
        elif json_status == "quick_reply":
            text = bot.get_received_text(all_json)
            ############ LOGS ##################################
            print("####### TEXT DATATYPE #######")
            print(type(text))
            print("####### TXT IS #######")
            print(text)
            print("####### RSP IS #######")
            print(bot_btns_agent(text))
            print('####### PAYLOAD ######')
            print(bot.get_quick_reply_payload(all_json))
            ####################################################
            bot.send_text_msgs(bot_btns_agent(text), "RESPONSE", recipient_id)
            if bot.get_quick_reply_payload(all_json) == 'START':
                get_started_msg = respond_to("GET_STARTED")[0]
                bot.quick_reply(get_started_msg, quick_reply_btns(), recipient_id)
        elif json_status == 'location':
            cord = bot.get_gps_coordinates()
            cord = (cord['lat'], cord['long'])
            response = bot_btns_agent("Via GPS", cord=cord)
            bot.send_text_msgs(response, "RESPONSE", recipient_id)
        bot.main_menu(recipient_id)
    return HttpResponse()


def quick_reply_btns():
    quick_replies = [
        {
            "content_type":"text",
            "title": "Via City" ,
            "payload": "QUICK_REPLY"
        },
        {
            "content_type":"location",
            "title": "Via GPS",
            "payload": "LOCATION"
        }
    ]
    return quick_replies
    