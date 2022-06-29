from django.contrib import admin
from django.urls import path,include
from .import settings
urlpatterns = [
    path('', include('TransiteApp.urls')),
    
    # url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
