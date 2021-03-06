# Generated by Django 3.2.10 on 2021-12-21 08:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("strategy", "0004_strategysharing"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScheduledStrategy",
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
                    "strategy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="strategy.strategy",
                    ),
                ),
            ],
        ),
    ]
