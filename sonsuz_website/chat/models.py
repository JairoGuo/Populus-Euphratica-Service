import uuid

from django.db import models
from django.conf import settings

# Create your models here.


class Message(models.Model):
    """用户间私信"""
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages',
                               blank=True, null=True, on_delete=models.SET_NULL, verbose_name='发送者')
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages',
                                  blank=True, null=True, on_delete=models.SET_NULL, verbose_name='接受者')
    message = models.TextField(blank=True, null=True, verbose_name='内容')
    unread = models.BooleanField(default=True, db_index=True, verbose_name='是否未读')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)

    class Meta:
        verbose_name = '私信'
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def __str__(self):
        return self.message

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()
