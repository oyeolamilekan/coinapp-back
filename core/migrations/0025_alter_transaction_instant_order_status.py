# Generated by Django 4.0.4 on 2022-05-11 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_transaction_instant_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='instant_order_status',
            field=models.CharField(choices=[('DONE', 'DONE'), ('CONFIRM', 'CONFIRM'), ('CANCELLED', 'CANCELLED')], default='DONE', max_length=300),
        ),
    ]
