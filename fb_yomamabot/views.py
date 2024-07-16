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

# recipient_id = '7812277818885789'


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        recipient_id = data.get('recipient_id')  # Assuming recipient ID is sent in the request body
        page_access_token = 'EAAGnLttZBmZCMBO5Tc8meqcpnA3pM7CfQy7hWCMpbYwDxaC77aocZBGmZAvehtOPGnUsuo8ZAlXYZAZBa2GDiZAb2BqMo9hL5mHfLUr96BfBt9Hjpgtorsk9K0H6xlZApDn5KOQCd8FQ6jjR4h8JcaBcunUp0BM7dvG4remfrR2Y10xmp8KP05IbMmDGKCEVHDlO9CoMOInqCZBQZDZD'
        recipient_id = '7812277818885789'
        post_message_url = f'https://graph.facebook.com/v20.0/me/messages'
        response_msg = {
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",  # Or "UPDATE" based on your use case
            "message": {"text": message}
        }

        response = requests.post(post_message_url, 
                                 params={"access_token": page_access_token},
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(response_msg))
        response_data = response.json()

        # Log the response for debugging
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Data: {response_data}")

        if response.status_code == 200:
            return JsonResponse({"status": "Message sent!"})
        else:
            return JsonResponse({"status": "Error", "details": response_data}, status=response.status_code)
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
