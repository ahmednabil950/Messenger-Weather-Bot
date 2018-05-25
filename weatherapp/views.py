from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from utils.messenger import messenger

def main_view(request):
    if request.method == 'GET':
        return bot_access_token(request)


def bot_access_token(request):
    bot = messenger()

    if request.method == 'GET': 
        token_sent = request.GET.get("hub.verify_token")
        if  bot.Verify_Token(token_sent):
            return HttpResponse(request.GET.get("hub.challenge"))
    return HttpResponse("Error")