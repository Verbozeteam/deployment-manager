# Generated by Django 2.0.3 on 2018-03-13 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0004_filedefaultparameter'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment',
            name='target',
            field=models.CharField(default='Room 128', max_length=256),
            preserve_default=False,
        ),
    ]
