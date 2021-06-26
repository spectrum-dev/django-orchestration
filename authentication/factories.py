import factory
import factory.fuzzy

from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp

from authentication.models import AccountWhitelist


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


def set_up_authentication():
    social_app = SocialAppFactory()

    user = UserFactory()

    social_account = SocialAccountFactory(user=user, provider=social_app)

    social_token_factory = SocialTokenFactory(app=social_app, account=social_account)

    return {"token": social_token_factory.token, "user": user}


class AccountWhitelistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccountWhitelist

    email = "valid@testcustomer.com"
    active = True
