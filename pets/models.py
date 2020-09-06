from datetime import date

from django.db import models


# Create your models here.
from django.urls import reverse


class Category(models.Model):
    """Категории"""
    scientific_name = models.CharField("Научный вид", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.scientific_name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Breeds(models.Model):
    """Породы"""
    name = models.CharField("Название породы", max_length=100)
    description = models.TextField("Особенности")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"


class Pets(models.Model):
    """Домашние питомцы"""
    name = models.CharField("Кличка", max_length=100)
    breed = models.ManyToManyField(Breeds, verbose_name="породы")
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    date_in_shelter = models.DateField("Дата поступления в приют", default=date.today)
    # workers = models.ManyToManyField()
    description = models.TextField("Описание")
    photo = models.ImageField("Фото", upload_to="pets/")
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("pets_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"


class PetShots(models.Model):
    """Фото питомцев"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Фото", upload_to="pets_shots/")
    pet = models.ForeignKey(Pets, verbose_name="Питомец", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фото питомца"
        verbose_name_plural = "Фото питомцев"


class ReviewWorkers(models.Model):
    """Отзывы сотрудников приюта"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        "self", verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    pet = models.ForeignKey(Pets, verbose_name="Питомец", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.pet}"

    class Meta:
        verbose_name = "Комментарий работника приюта"
        verbose_name_plural = "Комментарии работников приюта"
