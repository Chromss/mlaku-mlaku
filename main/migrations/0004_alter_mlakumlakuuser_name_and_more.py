# Generated by Django 5.1.1 on 2024-10-27 08:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_mlakumlakuuser_is_google_alter_mlakumlakuuser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlakumlakuuser',
            name='name',
            field=models.CharField(max_length=25, validators=[django.core.validators.MinLengthValidator(5)]),
        ),
        migrations.AlterField(
            model_name='mlakumlakuuser',
            name='password',
            field=models.CharField(max_length=40, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
        migrations.AlterField(
            model_name='mlakumlakuuser',
            name='username',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.MinLengthValidator(5)]),
        ),
    ]
