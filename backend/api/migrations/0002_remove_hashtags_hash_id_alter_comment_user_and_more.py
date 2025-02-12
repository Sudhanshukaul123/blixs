# Generated by Django 5.1.6 on 2025-02-12 07:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hashtags',
            name='hash_id',
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to='api.user'),
        ),
        migrations.AlterField(
            model_name='hashtags',
            name='tag',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
