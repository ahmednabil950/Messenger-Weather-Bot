from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from utils.messenger import messenger
from bot.bot import bot_agent
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

        quick_replies = [
            {
                "content_type":"text",
                "title": "Via City" ,
                "payload": "QUICK_REPLY"
            },
            {
                "content_type":"location",
                "title": "Via GPS",
                "payload": "QUICK_REPLY"
            }
        ]
        msg = "How would you like to get a weather forecast?"

        ###### Here the input is text from the chatbot #####
        ####################################################
        if json_status == "text":
            try:
                text = bot.get_received_text(all_json)
                text = str(text)
                content = bot_agent(text)
                print("####### TEXT DATATYPE #######")
                print(type(text))
                print("####### TXT IS #######")
                print(text)
                print("####### RSP IS #######")
                print(content)
                req_json, req_status = bot.send_text_msgs(
                    content, "RESPONSE", recipient_id)
            except requests.exceptions.Timeout:
                print("time out")
        ###### Here the input is get started button #####
        ####################################################
        elif json_status == "postback":
            postback = bot.get_postback(all_json)
            if postback.get('payload'):
                content = respond_to("FACEBOOK_WELCOME")
                bot.send_text_msgs(content, "RESPONSE", recipient_id)
            bot.quick_reply(msg, quick_replies, recipient_id)
        elif json_status == "quick_reply":
            print("####### TEXT DATATYPE #######")
            print(type(text))
            print("####### TXT IS #######")
            print(text)
            print("####### RSP IS #######")
            print(bot_agent(text))
            text = bot.get_received_text(all_json)
            bot.send_text_msgs(bot_agent(text), "RESPONSE", recipient_id)
    return HttpResponse()
