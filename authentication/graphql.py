from ariadne import SchemaDirectiveVisitor
from graphql import default_field_resolver, GraphQLError
from allauth.socialaccount.models import SocialToken


def get_user_context(request):
    context = {}
    context["request"] = request
    context["user"] = None

    # No token passed in - so no user assigned
    if "Authorization" not in request.headers:
        return context

    scheme, token = request.headers["Authorization"].split()

    # If not a bearer token - no user assigned
    if scheme.lower() != "bearer":
        return context

    try:
        social_token = SocialToken.objects.get(token=token)
        context["user"] = social_token.account.user
    except SocialToken.DoesNotExist:
        # Bearer token does not exist in DB
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
