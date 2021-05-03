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

import orchestrator.views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('orchestration/rest-auth/google/', orchestrator.views.GoogleLogin.as_view(), name='google_login')
    path('orchestration/metadata', orchestrator.views.get_all_metadata),
    path('orchestration/<block_type>/<block_id>/metadata', orchestrator.views.get_metadata),
    path('orchestration/<block_type>/<block_id>/<action_name>', orchestrator.views.proxy_block_action),
    path('orchestration/run', orchestrator.views.post_flow)
]
