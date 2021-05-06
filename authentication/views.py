from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, SocialLoginSerializer

# Create your views here.
# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter

@method_decorator(csrf_exempt, name='dispatch')
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)