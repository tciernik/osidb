# Generated by Django 3.2.15 on 2023-01-23 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osidb', '0066_tracker__alerts'),
    ]

    operations = [
        migrations.AddField(
            model_name='flawcomment',
            name='_alerts',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
