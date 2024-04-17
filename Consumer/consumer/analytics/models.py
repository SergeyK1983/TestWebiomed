from datetime import timedelta
from django.db import models
from django.db.models import Avg, Sum


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

    def get_total_nds(self, time_now):
        time_ = time_now - timedelta(hours=1)

        total_nds = Check.objects.filter(
            place_id=self.location.place_id,
            date_create__gte=time_
        ).aggregate(Sum('nds_amount'))
        return total_nds  # {'nds_amount__sum': Decimal('7.41')}

    def get_total_tips(self, time_now):
        time_ = time_now - timedelta(hours=1)

        total_tips = Check.objects.filter(
            place_id=self.location.place_id,
            date_create__gte=time_
        ).aggregate(Sum('tips_amount'))
        return total_tips  # {'tips_amount__sum': Decimal('7.41')}

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
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Сумма за время")
    average_receipt = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                          verbose_name="Средний чек по категории")

    class Meta:
        verbose_name = "Данные по категории"
        verbose_name_plural = "Данные по категориям"
        ordering = ["id", "cat"]

    def get_total_spent_and_average_receipt(self, time_now) -> dict:
        time_ = time_now - timedelta(hours=1)
        checks = Check.objects.filter(place_id=self.cat.location.place_id, date_create__gte=time_)
        total_spent = 0
        for var in checks:
            product = var.items.get(category=self.cat.category)
            total_cost = product.price * product.quantity
            total_spent += total_cost

        average_receipt = round(total_spent / len(checks), 2)

        return {"total_spent": total_spent, "average_receipt": average_receipt}

    def __str__(self):
        return f"Категории-аналитика: {self.cat}"
