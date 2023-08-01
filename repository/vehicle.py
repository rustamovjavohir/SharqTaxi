from django.shortcuts import get_object_or_404

from apps.vehicle.models import Car, DriverLicense


class VehicleRepository:
    def __init__(self):
        self.car = Car

    def get_car_by_number(self, number: str):
        return get_object_or_404(self.car, number=number)

    def create_car(self, **kwargs):
        return self.car.objects.create_car(**kwargs)

    def update_car(self, car, **kwargs):
        return self.car.objects.filter(id=car.id).update(**kwargs)


class DriverLicenseRepository:
    def __init__(self):
        self.driver_license = DriverLicense

    def get_driver_license_by_number(self, number: str):
        return get_object_or_404(self.driver_license, number=number)

    def create_driver_license(self, **kwargs):
        return self.driver_license.objects.create(**kwargs)

    def update_driver_license(self, driver_license, **kwargs):
        return self.driver_license.objects.filter(id=driver_license.id).update(**kwargs)
