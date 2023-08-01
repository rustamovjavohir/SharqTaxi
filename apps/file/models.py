from django.db import models
from utils.models import SlugModel, BaseModel


# Create your models here.


class Image(BaseModel):
    name = models.CharField(max_length=255,
                            null=True, blank=True,
                            verbose_name='Название')
    image = models.ImageField(upload_to='images',
                              verbose_name='Фото')
    is_main = models.BooleanField(default=False,
                                  verbose_name='Главное фото?')

    def __str__(self):
        return f"Image: {self.id.__str__()}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        file_name = ""
        if self.name:
            file_name = self.name + '.' + self.image.name.split('.')[-1]
        self.image.name = file_name
        return super(Image, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
