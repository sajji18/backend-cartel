"""
URL configuration for cartel project.

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
from django.urls import path, include
from django.views.generic import TemplateView
from authentication import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='authentication/index.html')),
    path('error/', TemplateView.as_view(template_name='authentication/errir.html')),

    path('user/login', views.OauthAuthorizeView.as_view(), name='oauth-authorize'),
    path('auth/callback/', views.OauthCallback.as_view(), name='oauth-callback'),
    path('auth/logout/', views.Logout.as_view(), name='auth-logout'),
    path('club/login/', views.ClubLoginView.as_view()),

    path('api/', include('authentication.urls')),
    path('api/', include('feed.urls')),
    path('info/',include('features.urls') ),
    path('book/',include("bookingsystem.urls")),
    

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
