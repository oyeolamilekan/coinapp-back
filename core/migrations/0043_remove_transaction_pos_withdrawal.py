# Generated by Django 4.0.4 on 2022-06-11 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_transaction_related_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='pos_withdrawal',
        ),
    ]
