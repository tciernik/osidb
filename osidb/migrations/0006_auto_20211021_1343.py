# Generated by Django 3.2.8 on 2021-10-21 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("osidb", "0005_auto_20211021_0931"),
    ]

    operations = [
        migrations.AlterField(
            model_name="affect",
            name="resolution",
            field=models.CharField(
                choices=[
                    ("NONE", "Novalue"),
                    ("FIX", "Fix"),
                    ("DEFER", "Defer"),
                    ("WONTFIX", "Wontfix"),
                    ("OOSS", "Ooss"),
                    ("DELEGATED", "Delegated"),
                    ("WONTREPORT", "Wontreport"),
                ],
                max_length=100,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="affectevent",
            name="resolution",
            field=models.CharField(
                choices=[
                    ("NONE", "Novalue"),
                    ("FIX", "Fix"),
                    ("DEFER", "Defer"),
                    ("WONTFIX", "Wontfix"),
                    ("OOSS", "Ooss"),
                    ("DELEGATED", "Delegated"),
                    ("WONTREPORT", "Wontreport"),
                ],
                max_length=100,
                null=True,
            ),
        ),
    ]
