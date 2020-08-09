from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from sonsuz_website.chat.consumers import MessagesConsumer, PushConsumer
# from sonsuz_website.notifications.consumers import NotificationsConsumer


# self.scope['type']获取协议类型
# self.scope['url_route']['kwargs']['username']获取url中关键字参数
# channels routing是scope级别的，一个连接只能由一个consumer接收和处理

application = ProtocolTypeRouter({
    # 普通的HTTP请求不需要我们手动在这里添加，框架会自动加载
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                # path('ws/notifications/', NotificationsConsumer),
                path('ws/<str:group_name>/', MessagesConsumer),
                path('push/<str:username>/', PushConsumer),
            ])
        )
    )
})

"""
OriginValidator或AllowedHostsOriginValidator可以防止通过WebSocket进行CSRF攻击
OriginValidator需要手动添加允许访问的源站，如：
from channels.security.websocket import OriginValidator

application = ProtocolTypeRouter({
    'websocket': OriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                ...
            ])
        ),
        [".mydjango.com", "http://.mydjango.com:80", "http://mydjango.site.com"]
    )
})
使用AllowedHostsOriginValidator，允许的访问的源站与settings.py文件中的ALLOWED_HOSTS相同
AuthMiddlewareStack用于WebSocket认证，集成了CookieMiddleware, SessionMiddleware,
AuthMiddleware, 兼容Django认证系统
"""
