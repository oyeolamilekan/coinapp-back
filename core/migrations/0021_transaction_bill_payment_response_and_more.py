# Generated by Django 4.0.4 on 2022-05-09 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_network_bills_network'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='bill_payment_response',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='transaction',
            name='instant_sell_response',
            field=models.JSONField(default=dict),
        ),
    ]
