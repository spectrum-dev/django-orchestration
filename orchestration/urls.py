"""orchestration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ariadne_django.views import GraphQLView
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.static import serve

import authentication.views
import orchestrator.views
from authentication.graphql import get_user_context
from orchestration.graphql_config import schema

urlpatterns = [
    url(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path(
        "graphql/",
        GraphQLView.as_view(schema=schema, context_value=get_user_context),
        name="graphql",
    ),
    path("orchestration/admin/", admin.site.urls),
    path(
        "rest-auth/google/",
        authentication.views.GoogleLogin.as_view(),
        name="google_login",
    ),
    url(r"^authentication/", include("allauth.urls"), name="socialaccount_signup"),
    path("orchestration/validate", orchestrator.views.ValidateFlow.as_view()),
    path(
        "orchestration/<block_type>/<block_id>/metadata",
        orchestrator.views.MetadataView.as_view(),
    ),
    path(
        "orchestration/<block_type>/<block_id>/<action_name>",
        orchestrator.views.ProxyBlockActionView.as_view(),
    ),
    path("orchestration/overlay", orchestrator.views.RunOverlay.as_view()),
]
