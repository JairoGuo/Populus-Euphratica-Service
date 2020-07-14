from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from sonsuz_website.chat.api.serializers import MessageSerializer
from sonsuz_website.chat.models import Message


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def create(self, request, *args, **kwargs):
        print(request.data)
        sender = request.user
        reciever_username = request.data['reciever']
        reciever = get_user_model().objects.get(username=reciever_username)
        message_content = request.data['message']
        if len(message_content.strip()) != 0 and sender != reciever:
            serializer = MessageSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'info': 'error'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            # msg = Message.objects.create(
            #     sender=sender,
            #     reciever=reciever,
            #     message=message_content
            # )
            channel_layer = get_channel_layer()
            payload = {
                'type': 'receive',
                'message': serializer.data,
                'sender': sender.username
            }
            # group_send(group: 所在组-接收者的username, message: 消息内容)
            async_to_sync(channel_layer.group_send)(reciever.username, payload)
            return Response(serializer.data)


        return Response({'message': 'ok'})
