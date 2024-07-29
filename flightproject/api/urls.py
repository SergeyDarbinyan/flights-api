from django.urls import path
from . import views

urlpatterns = [
    path(
        "flights/all/",
        views.AirOperatorAPIView.as_view(),
    ),
    path(
        "flights/permissions/",
        views.PermissionFlightsAPIView.as_view(),
    ),
    path(
        "flights/by-direction/",
        views.CountryFlightsAPIView.as_view(),
    ),
    path(
        "flights/from-one-to-seven/",
        views.AirOperatorTransportationAPIView.as_view(),
    ),
    path(
        "flights/frequency/",
        views.FrequentFlightsAPIView.as_view(),
    ),
]
