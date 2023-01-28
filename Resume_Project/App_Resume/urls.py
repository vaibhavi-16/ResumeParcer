from django.contrib import admin
from django.urls import path
from.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'App_Resume'


urlpatterns = [
    path('', home,name='home'),
    path('about/', about,name='about'),
]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
