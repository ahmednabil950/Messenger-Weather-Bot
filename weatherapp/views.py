from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from utils.messenger import messenger
from bot.bot import bot_agent
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

    if request.method == 'POST':
        
        all_json = json.loads(request.body.decode('utf-8'))
        
        postback = bot.get_postback(all_json)

        if postback.get('payload'):
            payload = postback.get('payload') or None
            if payload is not None:
                bot.send_text_msgs('Greetings !, I am a weather robot glad to help you to find the forecast')

        print("###### JSON FORMAT ######")
        recipient_id = bot.get_receptient_ID(all_json)
        print(all_json)
        
        print("###### JSON STATUS ######")
        json_status = bot.check_json_sent(all_json)
        print(json_status)

        if json_status == "text":
            try:
                text = bot.get_received_text(all_json)
                text = str(text)
                content = [
                    bot_agent(text)
                ]
                print("####### TEXT DATATYPE #######")
                print(type(text))
                print("####### TXT IS #######")
                print(text)
                req_json, req_status = bot.send_text_msgs(
                    content, "RESPONSE", recipient_id)
            except requests.exceptions.Timeout:
                print("time out")
            except AttributeError:
                pass
    return HttpResponse()
