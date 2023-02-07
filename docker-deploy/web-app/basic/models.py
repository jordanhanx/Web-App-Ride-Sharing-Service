from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.


def validate_datetime(datetime):
    if datetime < timezone.now():
        raise ValidationError("Datetime cannot be in the past")


class Driver(models.Model):
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, verbose_name=" ")
    first_name = models.CharField(verbose_name="First name", max_length=32)
    last_name = models.CharField(verbose_name="Last name", max_length=32)
    plate_nubmer = models.CharField(verbose_name="Plate number", max_length=32)
    veh_type = models.SmallIntegerField(verbose_name="Vehicle type", default=1,
                                        choices=[(1, "Hatchback"), (2, "MPV"), (3, "Pickup"), (4, "Sedan"), (5, "Sports"), (6, "SUV"), (7, "other")])
    capacity = models.PositiveSmallIntegerField(
        verbose_name="Capacity", validators=[MinValueValidator(1)])
    manufacturer = models.CharField(
        verbose_name="Manufacturer", max_length=32, blank=True)
    register_time = models.DateTimeField(
        verbose_name="Registered time", auto_now_add=True)
    vehicle_info = models.TextField(verbose_name="Vehicle info", blank=True)


class Ride(models.Model):
    status = models.SmallIntegerField(verbose_name="Ride status", default=1,
                                      choices=[(1, "Open"), (2, "Confirmed"), (3, "Complete")])
    created_time = models.DateTimeField(
        verbose_name="Created Time", auto_now_add=True)
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name=" ")
    driver = models.ForeignKey(
        to=Driver, on_delete=models.CASCADE, null=True, verbose_name=" ")
    start_point = models.CharField(verbose_name="Starting", max_length=256)
    destination = models.CharField(verbose_name="Destination", max_length=256)
    req_arrival_time = models.DateTimeField(
        verbose_name="Required Arrival Time", validators=[validate_datetime])
    passengers = models.PositiveSmallIntegerField(
        verbose_name="Passengers", validators=[MinValueValidator(1)])
    veh_type = models.SmallIntegerField(verbose_name="Vehicle type", default=0,
                                        choices=[(0, "Any"), (1, "Hatchback"), (2, "MPV"), (3, "Pickup"), (4, "Sedan"), (5, "Sports"), (6, "SUV"), (7, "other")])
    is_shared = models.SmallIntegerField(
        verbose_name="is shared", default=False, choices=[(1, "No"), (2, "Yes")])
    special_request = models.TextField(
        verbose_name="Special requests", blank=True)


class Sharer(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name=" ")
    ride = models.ForeignKey(
        to=Ride, on_delete=models.CASCADE, verbose_name=" ")
    party_passengers = models.PositiveSmallIntegerField(
        verbose_name="Sharer passengers", validators=[MinValueValidator(1)])
