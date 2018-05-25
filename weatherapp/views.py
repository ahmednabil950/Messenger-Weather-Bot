from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from utils.messenger import messenger
from django.views.decorators.csrf import csrf_exempt
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

        recipient_id = bot.Return_Reception_ID(all_json)
        json_status = bot.check_json_sent(all_json)

        print(json_status)

        if json_status == "text":

            try:
                content = ["Hello There !!"]
                text = bot.Return_Received_Text(all_json)
                text = str(text)
                print("#### TEXT DATATYPE #####")
                print(type(text))
                req_json, req_status = bot.Sent_text_Msgs(
                    content, "RESPONSE", recipient_id)
                print("####### TXT IS #####")
                print(text)

            except requests.exceptions.Timeout:
                print("time out")

    return HttpResponse("s")
