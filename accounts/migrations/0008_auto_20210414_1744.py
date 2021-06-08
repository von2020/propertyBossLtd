# Generated by Django 3.1.2 on 2021-04-14 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210414_1724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='gold',
        ),
        migrations.AddField(
            model_name='subscription',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plan', to='accounts.plan'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='name',
            field=models.CharField(default='', max_length=20, verbose_name='name'),
        ),
    ]