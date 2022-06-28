# Generated by Django 3.2.13 on 2022-05-09 19:25

from django.db import migrations, models
import psqlextra.fields.hstore_field


class Migration(migrations.Migration):

    dependencies = [
        ('osidb', '0046_affect_required_fields_revision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='external_system_id',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tracker',
            name='meta_attr',
            field=psqlextra.fields.hstore_field.HStoreField(default=dict),
        ),
        migrations.AlterField(
            model_name='tracker',
            name='ps_update_stream',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tracker',
            name='resolution',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tracker',
            name='status',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tracker',
            name='type',
            field=models.CharField(choices=[('JIRA', 'Jira'), ('BUGZILLA', 'Bz')], default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trackerevent',
            name='external_system_id',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trackerevent',
            name='meta_attr',
            field=psqlextra.fields.hstore_field.HStoreField(default=dict),
        ),
        migrations.AlterField(
            model_name='trackerevent',
            name='ps_update_stream',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trackerevent',
            name='resolution',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trackerevent',
            name='status',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trackerevent',
            name='type',
            field=models.CharField(choices=[('JIRA', 'Jira'), ('BUGZILLA', 'Bz')], default='', max_length=100),
            preserve_default=False,
        ),
    ]
