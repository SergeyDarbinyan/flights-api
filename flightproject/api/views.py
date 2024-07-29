from datetime import datetime, time

from django.db.models import Min, Max, Count, Q
from rest_framework import views, status
from rest_framework.request import Request
from rest_framework.response import Response

from .choices.airport_codes import AirportCode
from .choices.flight_directions import FlightDirection
from .models import Flights
from .serializers import (
    FlightsSerializer,
    AirOperatorViewSerializer,
    PermissionFlightsViewSerializer,
    ArmenianFlightsViewSerializer,
    AirOperatorTransportationViewSerializer,
    FrequentFlightSerializer,
)


class AirOperatorAPIView(views.APIView):
    def get(self, request: Request):
        serializer = AirOperatorViewSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        air_operator_name = serializer.data.get("air_operator", None)
        if air_operator_name is None:
            return Response(
                data={"message": "Failed to get air_operator_name"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        flights = list(Flights.objects.filter(airoperator_name=air_operator_name))
        response_data = FlightsSerializer(instance=flights, many=True).data
        return Response(data=response_data, status=status.HTTP_200_OK)


class PermissionFlightsAPIView(views.APIView):
    def get(self, request: Request):
        serializer = PermissionFlightsViewSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        date_from = serializer.data.get("date_from", None)
        date_to = serializer.data.get("date_to", None)
        if not date_from or not date_to:
            min_max_dates = Flights.objects.aggregate(
                min_date=Min("sign_date"), max_date=Max("sign_date")
            )

            if date_from is None:
                date_from = min_max_dates["min_date"] or datetime.min
            if date_to is None:
                date_to = min_max_dates["max_date"] or datetime.max

        flights = list(
            Flights.objects.filter(sign_date__gte=date_from, sign_date__lte=date_to)
        )
        response_data = FlightsSerializer(instance=flights, many=True).data
        return Response(data=response_data, status=status.HTTP_200_OK)


class CountryFlightsAPIView(views.APIView):
    def get(self, request: Request):
        serializer = ArmenianFlightsViewSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        flights_type = serializer.data.get("flight_type", None)
        if flights_type is None:
            return Response(
                data={"message": f"flights_type is required. Available options are: {', '.join([ft.value for ft in FlightDirection])}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if flights_type == FlightDirection.TO_ARMENIA.value:
            flights = Flights.objects.filter(arrival_1=AirportCode.YEREVAN.value)
        elif flights_type == FlightDirection.FROM_ARMENIA.value:
            flights = Flights.objects.filter(departure_1=AirportCode.YEREVAN.value)
        elif flights_type == FlightDirection.IN_ARMENIA.value:
            flights = Flights.objects.filter(
                arrival_1=AirportCode.YEREVAN.value,
                departure_1=AirportCode.YEREVAN.value,
            )
        else:
            return Response(
                data={
                    "message": "Invalid flights_type. Available options are: TO_ARMENIA, FROM_ARMENIA, IN_ARMENIA."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        response_data = FlightsSerializer(instance=flights, many=True).data
        return Response(data=response_data, status=status.HTTP_200_OK)


class AirOperatorTransportationAPIView(views.APIView):
    def get(self, request: Request):
        serializer = AirOperatorTransportationViewSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        air_operator_name = serializer.data.get("air_operator", None)
        if air_operator_name is None:
            return Response(
                data={"message": "Failed to get air_operator_name"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        time_from = time(1, 0)
        time_to = time(7, 0)

        flights = list(
            (
                Flights.objects.filter(
                    Q(airoperator_name=air_operator_name) &
                    Q(arrival_1_date_time__time__gte=time_from) &
                    Q(arrival_1_date_time__time__lte=time_to) &
                    Q(departure_1_date_time__time__gte=time_from) &
                    Q(departure_1_date_time__time__lte=time_to) &
                    ~Q(traffic_type='passenger')
                )
            )
        )

        response_data = FlightsSerializer(flights, many=True).data
        return Response(data=response_data, status=status.HTTP_200_OK)


class FrequentFlightsAPIView(views.APIView):
    def get(self, request: Request):
        frequent_flights = (
            Flights.objects.values("departure_1", "arrival_1")
            .annotate(
                flight_count=Count("uuid"),
                latest_arrival=Max("arrival_1_date_time"),
                latest_departure=Max("departure_1_date_time"),
            )
            .order_by("-flight_count")[:5]
        )

        response_data = FrequentFlightSerializer(frequent_flights, many=True).data
        return Response(data=response_data, status=status.HTTP_200_OK)
