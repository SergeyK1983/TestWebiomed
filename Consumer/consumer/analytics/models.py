from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Avg


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

# Приходящие чеки
class Check(models.Model):
    """ Чек """

    place_id = models.CharField(max_length=150, verbose_name="Идентификатор места")
    place_name = models.CharField(max_length=150, verbose_name="Название места покупки")
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="сумма чека")
    nds_amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="сумма НДС")
    tips_amount = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True,
                                      verbose_name="сумма чаевых")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')

    class Meta:
        verbose_name = "Чек"
        verbose_name_plural = "Чеки"
        ordering = ["id", "place_id"]

    def __str__(self):
        return f"Чек name: {self.place_name}"


class Product(models.Model):
    """ Продукт в чеке """

    quantity = models.IntegerField(verbose_name="количество")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="цена")
    category = models.CharField(max_length=150, verbose_name="категория")
    to_check = models.ForeignKey(to=Check, related_name="items", on_delete=models.CASCADE, verbose_name="Продукты")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["id", "category"]

    def __str__(self):
        return f"Продукт id: {self.id}, категория: {self.category}"


# Аналитика
class PurchaseLocation(models.Model):
    """ Место покупки """

    place_id = models.CharField(max_length=150, unique=True, verbose_name="Идентификатор места")
    place_name = models.CharField(max_length=150, verbose_name="Название места покупки")
    total_purchases = models.IntegerField(default=0, verbose_name="Кол-во покупок")
    average_receipt = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name="Средний чек")

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
        ordering = ["id", "place_id"]

    def get_total_purchases(self):
        total_purchases = Check.objects.filter(place_id=self.place_id).count()
        return total_purchases

    def get_average_receipt(self):
        average_receipt = Check.objects.filter(place_id=self.place_id).aggregate(Avg('total_amount'))
        return average_receipt

    def __str__(self):
        return f"Покупки от: {self.place_name}"


class Taxes(models.Model):
    """ Налоги и чаевые """

    location = models.ForeignKey(to=PurchaseLocation, to_field="place_id", related_name="taxes_amount",
                                 on_delete=models.CASCADE, verbose_name="Налоги и чаевые")
    total_nds = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Сумма НДС за время")
    total_tips = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Сумма чаевых за время")

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"
        ordering = ["id", "location"]

    def __str__(self):
        return f"Налоги от: {self.location}"


class Category(models.Model):
    """ Категории товаров в покупках """

    location = models.ForeignKey(to=PurchaseLocation, to_field="place_id", related_name="category_analytics",
                                 on_delete=models.CASCADE, verbose_name="место покупки")
    category = models.CharField(max_length=150, verbose_name="категория")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id", "location"]

    def __str__(self):
        return f"Категории: {self.location}"


class CategoryAnalytic(models.Model):
    """ Аналитика по категориям """

    cat = models.ForeignKey(to=Category, related_name="cat_analytics", on_delete=models.CASCADE,
                            verbose_name="Категории")
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма за время")
    average_receipt = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Средний чек по категории")

    class Meta:
        verbose_name = "Данные по категории"
        verbose_name_plural = "Данные по категориям"
        ordering = ["id", "cat"]

    def __str__(self):
        return f"Категории: {self.location}"
