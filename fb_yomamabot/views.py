# yomamabot/fb_yomamabot/views.py
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
import json
from pprint import pprint
import requests

class YoMamaBotView(View):
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
        return HttpResponse(status=200)

def chat_widget(request):
    return render(request, 'chat_widget.html')

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        # Your Facebook page access token
        page_access_token = 'EAAGnLttZBmZCMBOw56UDQBh2CuN2482Ukt4yVt5HHFyYZCOlQnFlTLdeFVGhniGZAc5GtOZAFTiVDwAK9khDTrrSYg6AC0ElkzZAkZCAaPQGb8eFdZB3sIrGw8mZCdIPih114yhlrFgQ7VvAxKSHGfF09VFxeWZCAXXcLNT2QfbspfEiQbPI4gtKj8xwkWRb7RhYIzScaJn0MUEwZDZD'
        # Your Facebook page ID
        recipient_id = '338795865991565'
        # Send the message to Facebook
        post_message_url = f'https://graph.facebook.com/v20.0/me/messages?access_token={page_access_token}'
        response_msg = json.dumps({
            "recipient": {"id": recipient_id},
            "message": {"text": message}
        })
        requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
        return JsonResponse({"status": "Message sent!"})
    return JsonResponse({"status": "Invalid request"}, status=400)









# # yomamabot/fb_yomamabot/views.py
# from django.shortcuts import render
# from django.views import generic
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.http import HttpResponse
# import json
# from pprint import pprint

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
