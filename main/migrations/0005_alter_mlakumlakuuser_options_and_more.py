# Generated by Django 5.1.1 on 2024-10-27 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_mlakumlakuuser_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mlakumlakuuser',
            options={},
        ),
        migrations.AlterModelManagers(
            name='mlakumlakuuser',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='mlakumlakuuser',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='mlakumlakuuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='mlakumlakuuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='mlakumlakuuser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='mlakumlakuuser',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='mlakumlakuuser',
            name='last_name',
        ),
    ]
