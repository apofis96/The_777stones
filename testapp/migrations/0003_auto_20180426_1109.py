# Generated by Django 2.0.4 on 2018-04-26 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_auto_20180420_2321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='OwnerID',
            new_name='ownerID',
        ),
        migrations.AlterField(
            model_name='game',
            name='isCompleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='game',
            name='secondPlayerID',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='winnerID',
            field=models.IntegerField(null=True),
        ),
    ]
