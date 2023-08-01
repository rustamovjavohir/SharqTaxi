from typing import Protocol

from django.test import TestCase


# Create your tests here.
class VehicleInterface(Protocol):

    def signal(self) -> str: ...

    def drive(self) -> str: ...

    def stop(self) -> str: ...


class Car:

    def __init__(self, name):
        self.name = name
        self.type = 'Car'

    def signal(self):
        return f'{self.name} bibibib'

    def drive(self):
        return f'{self.name} drive'

    def stop(self):
        return f'{self.name} stop'


class Truck:

    def __init__(self, name):
        self.name = name
        self.type = 'Truck'

    def signal(self):
        return f'{self.name} dididid papapap'

    def drive(self):
        return f'{self.name} drive'

    def stop(self):
        return f'{self.name} stop'


class VehicleService:

    def __init__(self, vehicle: VehicleInterface):
        self.vehicle = vehicle

    def signal(self):
        return self.vehicle.signal()

    def drive(self):
        return self.vehicle.drive()

    def stop(self):
        return self.vehicle.stop()


if __name__ == '__main__':
    service: VehicleInterface = Car('BMW')
    vehicle = Car('BMW')
    vehicle2 = Truck('KAMAZ')
    vehicle_service = VehicleService(vehicle2)
    print(vehicle_service.signal())

