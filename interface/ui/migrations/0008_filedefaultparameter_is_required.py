# Generated by Django 2.0.3 on 2018-03-13 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0007_auto_20180313_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='filedefaultparameter',
            name='is_required',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
