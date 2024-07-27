# yomamabot/fb_yomamabot/views.py


# fb_yomamabot/views.py
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import requests
from pprint import pprint

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

                    # Broadcast the message to WebSocket clients
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        'chat_chat_room',
                        {
                            'type': 'chat_message',
                            'message': message['message']['text'],
                        }
                    )
        return HttpResponse(status=200)

def chat_widget(request):
    return render(request, 'chat_widget.html')

# Send message
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        recipient_id = data.get('recipient_id')
        page_access_token = data.get('access_token')  # Get the access token from the request

        if not recipient_id or not page_access_token:
            return JsonResponse({"status": "Error", "details": "Recipient ID or Access Token missing"}, status=400)

        post_message_url = f'https://graph.facebook.com/v20.0/me/messages'
        response_msg = {
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
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





# load liste pages 
def fetch_pages(request):
    user_access_token = 'EAAGnLttZBmZCMBO8jkaICOcsh2EZA75p1relOaBu3tH1goZBjZBPo0Dh9q3P2OTDhqOFVesw5vNTZANELZACI0IQBgIk4T3jpX5W3Xdp8JiNUNoMW0jKY5yiRRnnvNGhImv2JSvnVN2PtJAIDWR2ZCjHBMD0vGJmXfJpXD12ZBGruj2pUxypNXEPuMCbP69wzRiZBwY1kHuyRF6qidJbLdWFj3KHZBZBvSigdBWfZC3UZD'  # Replace with your actual user access token
    user_id = '122103504482407107'  # Replace with your actual user ID
    url = f"https://graph.facebook.com/{user_id}/accounts"
    params = {
        'access_token': user_access_token,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        pages_data = response.json().get('data', [])
        return JsonResponse({'pages': pages_data})
    else:
        return JsonResponse({'error': 'Failed to fetch pages'}, status=response.status_code)


# load user liste 
def fetch_users(request):
    page_id = request.GET.get('page_id')
    access_token = request.GET.get('access_token')

    if not page_id or not access_token:
        return JsonResponse({'error': 'Page ID or Access Token missing'}, status=400)

    # Replace with actual URL to fetch users
    url = f"https://graph.facebook.com/{page_id}/conversations?platform=messenger&access_token={access_token}"

    response = requests.get(url)
    data = response.json()

    # Example processing of response data
    users = [{'id': conv['id'], 'name': 'User Name'} for conv in data.get('data', [])]  # Replace with actual user details
    return JsonResponse({'users': users})
