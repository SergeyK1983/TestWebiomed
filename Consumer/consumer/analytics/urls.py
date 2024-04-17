from django.urls import path
from .views import ChecksCreateAPIView

urlpatterns = [
    path('add_checks/', ChecksCreateAPIView.as_view(), name="checks"),
]
