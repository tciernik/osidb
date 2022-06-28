# Generated by Django 3.2.13 on 2022-04-25 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('osidb', '0033_fix_source_typos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='affectevent',
            name='cve_id',
        ),
        migrations.AlterUniqueTogether(
            name='affect',
            unique_together={('flaw', 'ps_module', 'ps_component')},
        ),
        migrations.RemoveField(
            model_name='affect',
            name='cve_id',
        ),
    ]
