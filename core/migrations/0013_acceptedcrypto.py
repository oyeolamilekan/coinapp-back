# Generated by Django 4.0.4 on 2022-05-05 14:41

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_transaction_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptedCrypto',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=300)),
                ('short_title', models.CharField(max_length=300)),
                ('is_live', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
    ]
