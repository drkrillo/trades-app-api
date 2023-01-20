# Generated by Django 3.2.16 on 2023-01-20 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20230117_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('datetime_id', models.DateTimeField(primary_key=True, serialize=False)),
                ('low', models.FloatField()),
                ('high', models.FloatField()),
                ('open', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.FloatField()),
                ('symbol', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.FloatField(default=1.0),
        ),
    ]