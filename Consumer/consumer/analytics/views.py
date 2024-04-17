from rest_framework import generics, status, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import Check, Product, PurchaseLocation, Taxes, Category, CategoryAnalytic
from .serializer import CheckSerializer


class ChecksCreateAPIView(generics.CreateAPIView):
    """ Прием чеков покупок. Запись в БД. """

    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]
    serializer_class = CheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





