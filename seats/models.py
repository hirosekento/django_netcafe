from django.db import models
from django.utils import timezone
import math

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price_per_hour = models.IntegerField(null=True, blank=True)
    flat_price = models.IntegerField(null=True, blank=True)
    flat_hours = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Seat(models.Model):
    number = models.PositiveIntegerField(unique=True)
    def __str__(self):
        return f"Seat {self.number}"

class Session(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

    def duration_hours(self):
        end = self.end_at or timezone.now()
        return (end - self.start_at).total_seconds() / 3600

    def calculate_price(self):
        hours = math.ceil(self.duration_hours())
        if self.plan.flat_price and self.plan.flat_hours:
            if hours <= self.plan.flat_hours:
                return self.plan.flat_price
            else:
                extra = hours - self.plan.flat_hours
                return self.plan.flat_price + math.ceil(extra) * (self.plan.price_per_hour or 300)
        return hours * (self.plan.price_per_hour or 300)

    def end_session(self):
        self.end_at = timezone.now()
        self.price = self.calculate_price()
        self.save()
