# Generated by Django 4.0.4 on 2022-05-02 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_billsrecharge_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=20),
        ),
    ]
