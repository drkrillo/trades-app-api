# Generated by Django 3.2.16 on 2023-01-24 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_order_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='title',
            field=models.CharField(default='<django.db.models.fields.CharField> order created on <django.db.models.fields.DateTimeField>', max_length=255),
        ),
    ]
