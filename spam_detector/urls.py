from django.urls import path
from .views import SpamDetectorView

app_name = 'spam_detector'

urlpatterns = [
    path('', SpamDetectorView.as_view(), name='index'),
]
