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

        bot.ACCESS_TOKEN = "EAAdfJWb1xs8BAJ1us9xi678ZBEMVDVv8cMQtvAcppW6ZCdjlzlYOkhBNoSqyZCfjxbwoFnYejy98k39nIlKyI2gcDZAuz8v4BpKuFgugOVYaAgl272VmAj5E1ot0jByYTTcUfswAiaIeppjpTmItZA2YWF12xNMIAbbKuA1I5ZCwZDZD"

        all_json = json.loads(request.body.decode('utf-8'))
        print("###### JSON FORMAT ######")
        print(all_json)
        recipient_id = bot.get_receptient_ID(all_json)
        json_status = bot.check_json_sent(all_json)
        print("###### JSON STATUS ######")
        print(json_status)

        messenger.quick_reply('text', ['text'], recipient_id)

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
        elif json_status == 'quick_reply':
            messenger.quick_reply('text', ['text'], recipient_id)

    return HttpResponse("s")
