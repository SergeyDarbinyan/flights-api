# Generated by Django 5.0.7 on 2024-07-28 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Flights",
            fields=[
                (
                    "uuid",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("created", models.TimeField(blank=True, max_length=10, null=True)),
                ("task_id", models.IntegerField(blank=True, null=True)),
                ("arrival_1", models.CharField(blank=True, max_length=3, null=True)),
                ("flight_no", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "sign_date",
                    models.DateTimeField(blank=True, max_length=255, null=True),
                ),
                (
                    "departure_1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "traffic_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "permission_no",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "airoperator_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "place_of_business",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "arrival_1_date_time",
                    models.DateTimeField(blank=True, max_length=255, null=True),
                ),
                (
                    "departure_1_date_time",
                    models.DateTimeField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "db_table": "Flights",
            },
        ),
    ]