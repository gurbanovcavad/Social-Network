# Generated by Django 5.1.4 on 2025-04-29 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_follow'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
    ]
