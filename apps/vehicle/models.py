from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from utils.choices import ColorChoices
from utils.models import SlugModel, BaseModel
from apps.file.models import Image


# Create your models here.

class CarManager(models.Manager):
    def create_car(self, **extra_fields):
        _car = self.model(**extra_fields)
        _car.save(using=self._db)
        return _car


class Brand(SlugModel):
    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'

    def __str__(self):
        return self.name


class DriverLicense(BaseModel):
    given_by = models.CharField(max_length=255, verbose_name='Кем выдан')
    number = models.CharField(max_length=255, verbose_name='Номер')
    date_of_issue = models.DateField(auto_now_add=True, verbose_name='Дата выдачи')
    date_of_expiration = models.DateField(auto_now_add=True, verbose_name='Дата истечения срока')
    image = models.ImageField(upload_to='vehicle/driver_license',
                              verbose_name='Фото водительского удостоверения')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Водительское удостоверение'
        verbose_name_plural = 'Водительские удостоверения'


class Car(SlugModel):
    name = models.CharField(max_length=255,
                            verbose_name='Название')
    number = models.CharField(max_length=8, unique=True,
                              verbose_name='Номер машины')
    year = models.IntegerField(verbose_name='Год выпуска',
                               validators=[MinValueValidator(1970), MaxValueValidator(2030)],
                               default=2020)
    color = models.CharField(max_length=255,
                             choices=ColorChoices.choices,
                             default=ColorChoices.WHITE,
                             verbose_name='Цвет')
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              verbose_name='Марка',
                              null=True, blank=True)
    main_image = models.ImageField(upload_to='vehicle/cars',
                                   null=True, blank=True,
                                   verbose_name='Главний фото машины')
    image = models.ManyToManyField(Image,
                                   verbose_name='Фото машины',
                                   related_name='car_image',
                                   blank=True)

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'
        ordering = ('-created_at',)

    objects = CarManager()

    def __str__(self):
        return self.name
