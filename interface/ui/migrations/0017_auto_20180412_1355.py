# Generated by Django 2.0.3 on 2018-04-12 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0016_repository_local_cache'),
    ]

    operations = [
        migrations.AddField(
            model_name='runningdeployment',
            name='stdout',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='runningdeployment',
            name='status',
            field=models.TextField(blank=True, default=''),
        ),
    ]