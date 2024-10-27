# Generated by Django 5.1 on 2024-10-25 14:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='journal',
            old_name='created_at',
            new_name='date_created',
        ),
        migrations.RemoveField(
            model_name='journal',
            name='author',
        ),
        migrations.RemoveField(
            model_name='journal',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='journal',
            name='saved_by',
        ),
        migrations.RemoveField(
            model_name='journal',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='journal',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='journal',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='main.journal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('journal', 'user')},
            },
        ),
        migrations.CreateModel(
            name='SavedJournal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_journals', to='main.journal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('journal', 'user')},
            },
        ),
    ]
