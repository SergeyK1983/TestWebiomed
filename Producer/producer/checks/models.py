from django.core.validators import MinValueValidator
from django.db import models


class Transaction(models.Model):
    """ Транзакция """

    transaction_id = models.CharField(max_length=150, unique=True, verbose_name="transaction_id")
    timestamp = models.DateTimeField(verbose_name="дата/время")
    total_amount = models.DecimalField(validators=[MinValueValidator(0.00)], max_digits=9, decimal_places=2,
                                       verbose_name="сумма чека")
    nds_amount = models.DecimalField(validators=[MinValueValidator(0.00)], max_digits=9, decimal_places=2,
                                     verbose_name="сумма НДС")
    tips_amount = models.DecimalField(validators=[MinValueValidator(0.00)], max_digits=9, decimal_places=2,
                                      null=True, blank=True, verbose_name="сумма чаевых")
    payment_method = models.CharField(max_length=20, verbose_name="метод оплаты")
    place_id = models.CharField(max_length=150, verbose_name="Идентификатор места")
    place_name = models.CharField(max_length=150, verbose_name="Название места покупки")

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ["id", "transaction_id"]

    def __str__(self):
        return f"Транзакция id: {self.transaction_id}, дата: {self.timestamp}"


class Product(models.Model):
    """ Продукт в транзакции """

    product_id = models.CharField(max_length=150, verbose_name="product_id")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="количество")
    price = models.DecimalField(validators=[MinValueValidator(0.00)], max_digits=9, decimal_places=2,
                                verbose_name="цена")
    category = models.CharField(max_length=150, verbose_name="категория")
    transaction = models.ForeignKey(to=Transaction, to_field="transaction_id", related_name="items",
                                    on_delete=models.CASCADE, verbose_name="Продукты")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["id", "product_id"]

    def __str__(self):
        return f"Продукт id: {self.product_id}"
