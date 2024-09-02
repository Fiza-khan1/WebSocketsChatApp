from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def return_user(token_string):
    try:
        user = Token.objects.get(key=token_string).user
    except Token.DoesNotExist:
        user = AnonymousUser()
    return user

class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_dict = parse_qs(query_string)

        # Default to AnonymousUser if 'token' is not in query_dict
        token = query_dict.get("token", [None])[0]
        user = await return_user(token) if token else AnonymousUser()

        scope["user"] = user
        return await self.app(scope, receive, send)
