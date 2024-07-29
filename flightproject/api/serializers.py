from rest_framework import serializers
from .models import Flights
from .choices.flight_directions import FlightDirection


class FlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flights
        fields = [
            "uuid",
            "created",
            "task_id",
            "arrival_1",
            "flight_no",
            "sign_date",
            "departure_1",
            "traffic_type",
            "permission_no",
            "airoperator_name",
            "place_of_business",
            "arrival_1_date_time",
            "departure_1_date_time",
        ]


class AirOperatorViewSerializer(serializers.Serializer):
    air_operator = serializers.CharField(max_length=100)


class PermissionFlightsViewSerializer(serializers.Serializer):
    date_from = serializers.DateTimeField(required=False)
    date_to = serializers.DateTimeField(required=False)

    def validate(self, data):
        date_from = data.get("date_from")
        date_to = data.get("date_to")

        if date_from and date_to and date_to < date_from:
            raise serializers.ValidationError(
                {"date_to": "date_to must be later than or equal to date_from."}
            )

        return data


class ArmenianFlightsViewSerializer(serializers.Serializer):
    flight_type = serializers.CharField(max_length=100, required=False)

    def validate_flight_type(self, value):
        if value is not None:
            value = value.upper()
            if value not in [ft.value for ft in FlightDirection]:
                raise serializers.ValidationError(
                    f"Invalid flight type. Available options are: {', '.join([ft.value for ft in FlightDirection])}."
                )
        return value


class AirOperatorTransportationViewSerializer(serializers.Serializer):
    air_operator = serializers.CharField(max_length=100)


class FrequentFlightSerializer(serializers.Serializer):
    departure_1 = serializers.CharField()
    arrival_1 = serializers.CharField()
    flight_count = serializers.IntegerField()
    latest_arrival = serializers.DateTimeField()
    latest_departure = serializers.DateTimeField()
