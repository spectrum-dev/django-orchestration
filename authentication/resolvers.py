from ariadne import convert_kwargs_to_snake_case
from django.db import IntegrityError

from authentication.models import AccountWhitelist

# Queries


def get_ping(*_):
    return "pong"


@convert_kwargs_to_snake_case
def get_account_whitelist_status(*_, email):
    try:
        AccountWhitelist.objects.get(
            email=email,
            active=True,
        )

        return {"status": True}
    except AccountWhitelist.DoesNotExist:
        return {"status": False}


# Mutations


@convert_kwargs_to_snake_case
def create_account_whitelist(*_, email):
    try:
        AccountWhitelist.objects.create(email=email, active=True)
        return {"status": True}
    except IntegrityError:
        return {"status": False}
