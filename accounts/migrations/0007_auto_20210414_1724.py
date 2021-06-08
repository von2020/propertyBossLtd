# Generated by Django 3.1.2 on 2021-04-14 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210413_1234'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Gold',
            new_name='Plan',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='premium',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='standard',
        ),
        migrations.DeleteModel(
            name='Premium',
        ),
        migrations.DeleteModel(
            name='Standard',
        ),
    ]
