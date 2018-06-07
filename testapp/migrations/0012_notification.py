# Generated by Django 2.0.4 on 2018-06-07 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testapp', '0011_game_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notificationType', models.CharField(max_length=1)),
                ('gameID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificationGame', to='testapp.Game')),
                ('playerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
