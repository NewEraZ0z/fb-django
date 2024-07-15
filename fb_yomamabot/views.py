

import json
import requests
from pprint import pprint
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

class YoMamaBotView(generic.View):
    def get(self, request, *args, **kwargs):
        hub_verify_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if hub_verify_token == '6698547781455':
            return HttpResponse(hub_challenge, status=200)
        else:
            return HttpResponse('Error, invalid token', status=403)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    pprint(message)
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        'chat_room1',  # dynamically generate based on user/page
                        {
                            'type': 'chat_message',
                            'message': message['message']['text']
                        }
                    )
        return HttpResponse(status=200)

def get_conversations(request):
    page_id = "YOUR_PAGE_ID"
    access_token = "YOUR_PAGE_ACCESS_TOKEN"
    platform = request.GET.get('platform', 'messenger')
    
    url = f"https://graph.facebook.com/v12.0/{page_id}/conversations"
    params = {
        'platform': platform,
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    return JsonResponse(response.json())

def get_messages(request, conversation_id):
    access_token = "YOUR_PAGE_ACCESS_TOKEN"
    
    url = f"https://graph.facebook.com/v12.0/{conversation_id}"
    params = {
        'fields': 'messages',
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    return JsonResponse(response.json())

def get_message_details(request, message_id):
    access_token = "YOUR_PAGE_ACCESS_TOKEN"
    
    url = f"https://graph.facebook.com/v12.0/{message_id}"
    params = {
        'fields': 'id,created_time,from,to,message',
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    return JsonResponse(response.json())








# # yomamabot/fb_yomamabot/views.py
# from django.shortcuts import render
# from django.views import generic
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.http import HttpResponse
# import json
# from pprint import pprint


# def dashboard(request):
#     return render(request, 'dashboard.html')

# class YoMamaBotView(generic.View):
#     def get(self, request, *args, **kwargs):
#         hub_verify_token = request.GET.get('hub.verify_token')
#         hub_challenge = request.GET.get('hub.challenge')
#         if hub_verify_token == '6698547781455':
#             return HttpResponse(hub_challenge, status=200)
#         else:
#             return HttpResponse('Error, invalid token', status=403)

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     # Post function to handle Facebook messages
#     def post(self, request, *args, **kwargs):
#         # Converts the text payload into a python dictionary
#         incoming_message = json.loads(request.body.decode('utf-8'))
#         # Facebook recommends going through every entry since they might send
#         # multiple messages in a single call during high load
#         for entry in incoming_message['entry']:
#             for message in entry['messaging']:
#                 # Check to make sure the received call is a message call
#                 # This might be delivery, optin, postback for other events
#                 if 'message' in message:
#                     # Print the message to the terminal
#                     pprint(message)
#         return HttpResponse(status=200)
