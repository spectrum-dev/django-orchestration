import factory

from authentication.models import AccountWhitelist


class AccountWhitelistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccountWhitelist

    email = "valid@testcustomer.com"
    active = True
