# Generated by Django 4.0.4 on 2022-05-02 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_billsrecharge_recieving_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='billsrecharge',
            name='is_redeemed',
            field=models.BooleanField(default=False),
        ),
    ]
