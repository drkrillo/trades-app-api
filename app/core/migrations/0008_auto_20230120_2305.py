# Generated by Django 3.2.16 on 2023-01-20 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20230120_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto',
            name='datetime_id',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='symbol',
            field=models.CharField(max_length=10),
        ),
    ]