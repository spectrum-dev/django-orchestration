from allauth.socialaccount.models import SocialToken
from ariadne import SchemaDirectiveVisitor
from graphql import GraphQLError, default_field_resolver

from .exceptions import InvalidTokenSchemeException
from .models import BasicAuthToken


def get_user_context(request):
    context = {}
    context["request"] = request
    context["user"] = None

    # No token passed in - so no user assigned
    if "Authorization" not in request.headers:
        return context

    scheme, token = request.headers["Authorization"].split()

    # If not a bearer or basic token - no user assigned
    if scheme.lower() != "bearer" and scheme.lower() != "basic":
        return context

    try:
        if scheme.lower() == "bearer":
            social_token = SocialToken.objects.get(token=token)
            context["user"] = social_token.account.user
        elif scheme.lower() == "basic":
            basic_auth_token = BasicAuthToken.objects.get(token=token)
            context["user"] = basic_auth_token.user
        else:
            raise InvalidTokenSchemeException
    except SocialToken.DoesNotExist:
        # Bearer token does not exist in DB
        return context
    except BasicAuthToken.DoesNotExist:
        # Basic token does not exist in DB
        return context
    except InvalidTokenSchemeException:
        # Scheme does not exist
        return context

    return context


class IsAuthenticatedDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, object_type):
        original_resolver = field.resolve or default_field_resolver

        def resolve_is_authenticated(obj, info, **kwargs):
            user = info.context.get("user")
            if user is None:
                raise GraphQLError(message="User is not authenticated")

            return original_resolver(obj, info, **kwargs)

        field.resolve = resolve_is_authenticated
        return field
