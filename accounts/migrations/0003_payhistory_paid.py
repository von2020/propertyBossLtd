# Generated by Django 3.1.2 on 2021-06-28 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210628_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='payhistory',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
