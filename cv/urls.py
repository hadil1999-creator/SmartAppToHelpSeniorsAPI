from django.urls import path
from . import views

app_name = 'cv'
urlpatterns = (
    path("image4analysis", views.image4analysis, name='image4analysis'),
)
