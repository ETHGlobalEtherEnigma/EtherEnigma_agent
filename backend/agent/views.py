from rest_framework.views import APIView
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from swarm import Swarm
from django.http import JsonResponse
from .agents import based_agent
import json

client = Swarm()
agentvar = based_agent
messages = []

@api_view(['POST'])
def gpt_view(request):
    global agentvar
    global messages
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('messages', [])
            if not message:
                return JsonResponse({'error': 'No messages provided'}, status=400)
            
            user_message = message[-1]
            messages.append({"role": "user", "content": user_message['content']})

            response = client.run(
                agent=agentvar, # type: ignore
                messages=messages,
                context_variables=None or {},
                stream=False,
                debug=False,
            )
            messages.extend(response.messages)
            agentvar = response.agent # type: ignore

            return JsonResponse({'messages': response.messages[0]})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

class GptView(View):
    agentvar = based_agent
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            messages = data.get('messages', [])
            if not messages:
                return JsonResponse({'error': 'No messages provided'}, status=400)

            user_message = messages[-1]
            messages = []
            messages.append({"role": "user", "content": user_message['content']})

            response = client.run(
                agent=self.agentvar, # type: ignore
                messages=messages,
                context_variables=None or {},
                stream=False,
                debug=False,
            )
            messages.extend(response.messages)
            self.agentvar = response.agent

            return JsonResponse({'messages': response.messages[0]})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        return JsonResponse({'error': 'Method not allowed'}, status=405)

@api_view(['POST'])
def echo_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            messages = data.get('messages', [])

            if not messages:
                return JsonResponse({'error': 'No messages provided'}, status=400)

            user_message = messages[-1]  # Get the last message from the user

            # Simulate an AI response
            ai_response = {
                "role": "assistant",
                "content": f"You said: {user_message['content']}"  # Echoing back the user's message
            }

            return JsonResponse({'messages': messages + [ai_response]})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
