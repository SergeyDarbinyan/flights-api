from django.db import models


class Flights(models.Model):
    uuid = models.CharField(max_length=255, primary_key=True)
    created = models.TimeField(max_length=10, blank=True, null=True)
    task_id = models.IntegerField(blank=True, null=True)
    arrival_1 = models.CharField(max_length=3, blank=True, null=True)
    flight_no = models.CharField(max_length=20, blank=True, null=True)
    sign_date = models.DateTimeField(max_length=255, blank=True, null=True)
    departure_1 = models.CharField(max_length=255, blank=True, null=True)
    traffic_type = models.CharField(max_length=255, blank=True, null=True)
    permission_no = models.CharField(max_length=255, blank=True, null=True)
    airoperator_name = models.CharField(max_length=255, blank=True, null=True)
    place_of_business = models.CharField(max_length=255, blank=True, null=True)
    arrival_1_date_time = models.DateTimeField(max_length=255, blank=True, null=True)
    departure_1_date_time = models.DateTimeField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.uuid

    class Meta:
        db_table = "Flights"
