# Generated by Django 5.0 on 2023-12-16 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productprice',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
