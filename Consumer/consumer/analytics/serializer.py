from rest_framework import serializers
from .models import Check, Product, PurchaseLocation, Taxes, Category, CategoryAnalytic


class ProductSerializer(serializers.ModelSerializer):
    """ Продукты в чеке """

    class Meta:
        model = Product
        fields = ["quantity", "price", "category"]


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


class PurchaseLocationSerializer(serializers.ModelSerializer):
    """ Список мест покупок """
    class Meta:
        model = PurchaseLocation
        fields = ["place_id", "place_name", "date_create"]


class TaxesSerializer(serializers.ModelSerializer):
    """ Налоги и чаевые """

    class Meta:
        model = Taxes
        fields = ["total_nds", "total_tips", "date_create"]


class CategoryAnalyticSerializer(serializers.ModelSerializer):
    """ Аналитика по категориям """

    class Meta:
        model = CategoryAnalytic
        fields = ["total_spent", "average_receipt", "date_create"]


class CategorySerializer(serializers.ModelSerializer):
    """ Категории товаров в покупках """

    cat_analytics = CategoryAnalyticSerializer(many=True)

    class Meta:
        model = Category
        fields = ["category", "cat_analytics"]


class AnalyticSerializer(serializers.ModelSerializer):
    """ Общая аналитика """

    taxes_amount = TaxesSerializer(many=True)
    category_analytics = CategorySerializer(many=True)

    class Meta:
        model = PurchaseLocation
        fields = ["place_id", "place_name", "place_name", "total_purchases", "taxes_amount", "category_analytics"]
