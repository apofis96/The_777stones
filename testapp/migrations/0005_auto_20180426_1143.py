# Generated by Django 2.0.4 on 2018-04-26 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_auto_20180426_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gameName',
            field=models.CharField(default='NoNameGame', max_length=100),
        ),
    ]
