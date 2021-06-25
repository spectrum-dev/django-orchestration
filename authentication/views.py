import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework import serializers

from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, SocialLoginSerializer

from authentication.models import AccountWhitelist

# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class ValidateAccountWhitelistView(APIView):
    def post(self, request):
        class PayloadSerializer(serializers.Serializer):
            email = serializers.EmailField(required=True)

            def validate(self, data):
                if not data["email"]:
                    raise serializers.ValidationError("Email must have a value")

                return data

        request_body = json.loads(request.body)
        PayloadSerializer(data=request_body).is_valid(raise_exception=True)

        account_exists = (
            AccountWhitelist.objects.all()
            .filter(email=request_body["email"])
            .filter(active=True)
            .exists()
        )
        status_code = 200
        if not account_exists:
            status_code = 401

        return JsonResponse({"status": account_exists}, status=status_code)
