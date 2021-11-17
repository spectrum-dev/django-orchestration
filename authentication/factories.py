import factory
import factory.fuzzy
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib.auth.models import User

from authentication.models import AccountWhitelist, BasicAuthToken


class SocialAppFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SocialApp

    provider = 1
    name = "Test Google Setup"
    client_id = "test.apps.googleusercontent.com"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.fuzzy.FuzzyText(length=12)
    password = factory.fuzzy.FuzzyText(length=24)


class SocialAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SocialAccount

    uid = factory.fuzzy.FuzzyText(length=24)


class SocialTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SocialToken

    token = factory.fuzzy.FuzzyText(length=12)


class BasicAuthTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BasicAuthToken

    token = factory.fuzzy.FuzzyText(length=12)


def set_up_authentication():
    social_app = SocialAppFactory()
    user = UserFactory()
    social_account = SocialAccountFactory(user=user, provider=social_app)
    social_token_factory = SocialTokenFactory(app=social_app, account=social_account)

    return {"token": social_token_factory.token, "user": user}


def set_up_basic_authentication():
    user = UserFactory()
    basic_auth_token = BasicAuthTokenFactory(user=user)

    return {"token": basic_auth_token.token, "user": user}


class AccountWhitelistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccountWhitelist

    email = "valid@testcustomer.com"
    active = True
