# Generated by Django 4.0.4 on 2022-05-13 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_transaction_instant_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='billsrecharge',
            name='blockchain_deposit_status',
            field=models.CharField(blank=True, choices=[('CONFIRMED', 'CONFIRMED'), ('REJECTED', 'REJECTED'), ('CONFIRMATION', 'CONFIRMATION')], max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='billsrecharge',
            name='is_overpaid',
            field=models.BooleanField(default=False),
        ),
    ]
