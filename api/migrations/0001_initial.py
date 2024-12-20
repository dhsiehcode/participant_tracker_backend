# Generated by Django 5.1 on 2024-10-30 02:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Participant",
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
                ("first_name", models.CharField(max_length=20)),
                ("last_name", models.CharField(max_length=20)),
                ("dob", models.DateField(verbose_name="date of birth")),
                ("sex", models.CharField(max_length=10)),
                ("occupation", models.CharField(max_length=20)),
                ("email", models.CharField(max_length=50)),
                (
                    "email_list",
                    models.BooleanField(
                        default=False, verbose_name="agreed to be on email list"
                    ),
                ),
                (
                    "collect_data",
                    models.BooleanField(
                        default=False,
                        verbose_name="agreed to have data for all experiment collected",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Resercher",
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
                ("first_name", models.CharField(max_length=20)),
                ("last_name", models.CharField(max_length=20)),
                (
                    "start_date",
                    models.DateField(
                        verbose_name="day this researcher started at the lab"
                    ),
                ),
                (
                    "end_date",
                    models.DateField(
                        verbose_name="day this researcher ended at the lab"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Experiment",
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
                (
                    "name",
                    models.CharField(max_length=50, verbose_name="name of experiment"),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=200, verbose_name="description of experiment"
                    ),
                ),
                (
                    "start_date",
                    models.DateField(
                        verbose_name="the first day the experiment is run"
                    ),
                ),
                (
                    "end_date",
                    models.DateField(verbose_name="the last day the experiment is run"),
                ),
                (
                    "irb_number",
                    models.CharField(max_length=50, verbose_name="irb protocol number"),
                ),
                (
                    "experimenter",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.resercher",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Participant_Experiment",
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
                (
                    "collect_data",
                    models.BooleanField(
                        null=True,
                        verbose_name="if we can collect data for this participant in this experiment",
                    ),
                ),
                (
                    "experiment_date",
                    models.DateField(
                        verbose_name="date experiment with this participant is conducted"
                    ),
                ),
                ("location", models.CharField(max_length=20)),
                (
                    "experiment_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="api.experiment"
                    ),
                ),
                (
                    "participant_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="api.participant",
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("participant_id", "experiment_id"),
                        name="unique experiment participant",
                    )
                ],
            },
        ),
    ]
