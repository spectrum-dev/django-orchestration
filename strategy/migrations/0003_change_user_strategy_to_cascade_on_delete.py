# Generated by Django 3.2.4 on 2021-07-20 07:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('strategy', '0002_implement_strategy_naming'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strategy',
            name='strategy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='strategy_strategy', to='strategy.userstrategy'),
        ),
        migrations.AlterField(
            model_name='userstrategy',
            name='user',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
