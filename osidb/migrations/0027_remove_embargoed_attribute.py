# Generated by Django 3.2.11 on 2022-02-01 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('osidb', '0026_trackers_many_affects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flaw',
            name='embargoed',
        ),
        migrations.RemoveField(
            model_name='flawevent',
            name='embargoed',
        ),
        migrations.RemoveField(
            model_name='flawhistory',
            name='embargoed',
        ),
    ]
