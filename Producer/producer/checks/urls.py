from django.urls import path
from .views import TransactionCreateAPIView, TransList

urlpatterns = [
    path('checks/', TransactionCreateAPIView.as_view(), name="checks"),
    path('ch/', TransList.as_view()),
]
