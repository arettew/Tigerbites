# Generated by Django 2.0.2 on 2018-04-17 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_auto_20180417_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fooditem',
            name='id',
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='item_name',
            field=models.CharField(default='', max_length=100, primary_key=True, serialize=False),
        ),
    ]
