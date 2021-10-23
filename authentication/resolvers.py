from ariadne import convert_kwargs_to_snake_case
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
