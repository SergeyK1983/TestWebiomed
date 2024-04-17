from rest_framework import serializers
from .models import Check, Product, PurchaseLocation, Taxes, Category, CategoryAnalytic


class ProductSerializer(serializers.ModelSerializer):
    """ Продукты в чеке """

    class Meta:
        model = Product
        fields = ["quantity", "price", "category"]


# {
#     "transaction_id": "unique_transaction_id17",
#     "timestamp": "2024-02-07T12:34:56",
#     "items": [
#         {
#             "product_id": "product_id_1",
#             "quantity": 2,
#             "price": 0,
#             "category": "groceries"
#         },
#         {
#             "product_id": "product_id_2",
#             "quantity": 1,
#             "price": 5.49,
#             "category": "electronics"
#         }
#     ],
#     "total_amount": 0,
#     "nds_amount": 2.47,
#     "tips_amount": 3.0,
#     "payment_method": "credit_card"
#     "place_id": ""
#     "place_name": ""
# }


class CheckSerializer(serializers.ModelSerializer):
    """ Приходящий чек """

    items = ProductSerializer(many=True)

    class Meta:
        model = Check
        fields = ["place_id", "place_name", "total_amount", "nds_amount", "tips_amount", "items"]

    def create(self, validated_data):
        items = validated_data.pop("items", [])
        instance = Check.objects.create(**validated_data)

        list(map(lambda x: x.update({"to_check": instance}), items))
        products = [Product(**items[i]) for i in range(len(items))]
        Product.objects.bulk_create(products)

        return instance



