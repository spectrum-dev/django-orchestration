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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.views.generic.base import View

from ariadne_django.views import GraphQLView

from orchestration.graphql_config import schema
from authentication.graphql import get_user_context

import strategy.views
import orchestrator.views
import authentication.views

urlpatterns = [
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
    path(
        "authentication/validate",
        authentication.views.ValidateAccountWhitelistView.as_view(),
    ),
    path("orchestration/metadata", orchestrator.views.AllMetadataView.as_view()),
    path(
        "orchestration/<block_type>/<block_id>/metadata",
        orchestrator.views.MetadataView.as_view(),
    ),
    path(
        "orchestration/<block_type>/<block_id>/<action_name>",
        orchestrator.views.ProxyBlockActionView.as_view(),
    ),
    path("orchestration/validate", orchestrator.views.ValidateFlow.as_view()),
    path("orchestration/run", orchestrator.views.RunFlow.as_view()),
    path("orchestration/overlay", orchestrator.views.RunOverlay.as_view()),
    path("strategy/strategyId", strategy.views.StrategyIdView.as_view()),
    path("strategy/createStrategy", strategy.views.CreateStrategyView.as_view()),
    path(
        "strategy/deleteStrategy/<strategy_id>",
        strategy.views.DeleteStrategyView.as_view(),
    ),
    path("strategy/getStrategies", strategy.views.GetAllStrategiesView.as_view()),
    path("strategy/<strategy_id>", strategy.views.StrategyView.as_view()),
    path("strategy/<strategy_id>/detail", strategy.views.StrategyDetailView.as_view()),
    path("strategy/<strategy_id>/commitId", strategy.views.CommitIdView.as_view()),
    path(
        "strategy/<strategy_id>/<commit_id>",
        strategy.views.StrategyCommitView.as_view(),
    ),
]
