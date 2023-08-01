"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.documentation import include_docs_urls
from django.conf import settings

api = [
    path('bot/', include("Bot.urls")),
    path('chat/', include("Chat.urls")),
    path('user/', include("User.urls")),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title="Api Docs", public=False, permission_classes=[AllowAny])),
    path('api/v1/', include(api))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)