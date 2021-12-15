# Generated by Django 3.2.10 on 2021-12-14 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("strategy", "0004_strategysharing"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScheduledUserStrategy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("last_run_at", models.DateTimeField(blank=True, null=True)),
                ("next_run_at", models.DateTimeField(blank=True, null=True)),
                ("cron_expression", models.CharField(max_length=200)),
                (
                    "user_strategy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="strategy.userstrategy",
                    ),
                ),
            ],
        ),
    ]
