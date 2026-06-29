from django.shortcuts import render
from django.views import View
import json
from django.views import View
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Messages


# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')

@method_decorator(csrf_exempt, name="dispatch")
class SendView(View):

    def post(self, request):
        data = json.loads(request.body)
        message = data.get("message")

        Messages.objects.create(message=message)
        
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "chat_global",
            {
                "type": "chat_message",
                "message": message
            }
        )

        return JsonResponse({"status": "ok"})
