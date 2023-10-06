# Generated by Django 3.2.7 on 2023-09-23 14:14

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='red_code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh1234567890', length=10, max_length=10, prefix='217', unique=True),
        ),
    ]
