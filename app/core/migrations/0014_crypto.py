# Generated by Django 3.2.16 on 2023-01-20 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_delete_crypto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField()),
                ('low', models.FloatField()),
                ('high', models.FloatField()),
                ('open', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.FloatField()),
                ('symbol', models.CharField(max_length=10)),
            ],
        ),
    ]
