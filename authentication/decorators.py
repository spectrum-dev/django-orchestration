from allauth.socialaccount.models import SocialToken
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission


# Authentication Classes
class SpectrumAuthentication(BasicAuthentication):
    def authenticate(self, request):
        bearer_token = request.headers["Authorization"].split(" ")[1]
        social_token_object = SocialToken.objects.filter(token=bearer_token)
        if len(social_token_object) == 0:
            raise AuthenticationFailed("The token provided is invalid.")

        user = social_token_object[0].account.user
        return (user, bearer_token)


# Permission Classes
class SpectrumIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        bearer_token = request.headers["Authorization"].split(" ")[1]
        social_token_object = SocialToken.objects.filter(token=bearer_token)
        return len(social_token_object) == 1
