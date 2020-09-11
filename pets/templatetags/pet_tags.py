from django import template

from pets.models import Category, Pets


register = template.Library()


@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


@register.inclusion_tag('pets/tags/last_pets.html')
def get_last_pets(count):
    pets = Pets.objects.order_by("id")[:count]
    return {"last_pets": pets}
