from django.urls import path
from . import views

app_name = 'speech'
urlpatterns = [
    path('text2speech', views.text2speech, name='text2speech'),
    path('speech2text', views.speech2text, name='speech2text'),
    path('talk', views.talk, name='talk'),
    path('talk_audio', views.talk_audio, name='talk_audio'),
]
