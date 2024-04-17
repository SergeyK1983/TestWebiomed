# Generated by Django 5.0.4 on 2024-04-17 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_product_total_cost_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Общая стоимость'),
        ),
    ]
