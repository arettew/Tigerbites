# Generated by Django 2.0.2 on 2018-05-08 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_auto_20180508_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='dhall',
            field=models.CharField(default='', max_length=200),
        ),
    ]
