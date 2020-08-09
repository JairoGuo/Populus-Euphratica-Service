from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from sonsuz_website.chat.api.serializers import MessageSerializer
from sonsuz_website.chat.models import Message


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('sender', 'receiver')

    def list(self, request, *args, **kwargs):

        # queryset = self.filter_queryset(self.get_queryset())
        queryset = self.get_queryset().filter((Q(sender=request.user.pk)| Q(sender=request.query_params['receiver']))
                                              & (Q(receiver=request.user.pk)
                                                 | Q(receiver=request.query_params['receiver']))).order_by('created_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # print(request.data)
        data = dict(request.data)
        sender = request.user
        receiver_username = data['receiver']
        receiver = get_user_model().objects.get(username=receiver_username)
        message_content = request.data['message']
        data.update({'sender': sender.pk})
        data.update({'receiver': receiver.pk})
        if len(message_content.strip()) != 0 and sender != receiver:
            # print(data)
            serializer = MessageSerializer(data=data)
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
                'type': 'receive.json',
                'message': serializer.data,
                'sender': sender.username
            }
            # group_send(group: 所在组-接收者的username, message: 消息内容)
            async_to_sync(channel_layer.group_send)('c4103f122d27677c9db144cae1394a66', payload)
            return Response(serializer.data)

        return Response({'message': 'prohibit'})

    @action(detail=False, methods=["GET"])
    def get_recent_conversation(self, request):
        user = get_user_model().objects.get(username=request.user.username)
        instance = Message.objects.filter(sender=user.pk).order_by('-created_at').distinct()
        i = Message.objects.values('receiver').filter(sender=user.pk).annotate().order_by('-created_at').distinct()
        print(i)
        serializer = self.get_serializer(instance, many=True)

        return Response(serializer.data)

