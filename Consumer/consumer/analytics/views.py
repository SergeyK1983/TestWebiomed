from rest_framework import generics, status, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import Check, Product, PurchaseLocation, Taxes, Category, CategoryAnalytic
from .serializer import CheckSerializer, PurchaseLocationSerializer, AnalyticSerializer
from .services import create_purchase_or_add_category


class PurchaseListAPIView(generics.ListAPIView):
    """ Список мест покупок """

    permission_classes = [permissions.AllowAny]
    serializer_class = PurchaseLocationSerializer
    queryset = PurchaseLocation.objects.all()


class AnalyticListAPIView(generics.ListAPIView):
    """ Общая аналитика """

    permission_classes = [permissions.AllowAny]
    serializer_class = AnalyticSerializer
    queryset = PurchaseLocation.objects.all()


class ChecksCreateAPIView(generics.CreateAPIView):
    """ Прием чеков покупок. Запись в БД. """

    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]
    serializer_class = CheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        create_purchase_or_add_category(instance)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





