# Generated by Django 3.2.16 on 2023-01-20 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_crypto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.FloatField(null=True),
        ),
    ]
