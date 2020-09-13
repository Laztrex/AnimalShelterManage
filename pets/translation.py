from modeltranslation.translator import register, TranslationOptions
from .models import Category, Pets, Breeds, PetShots


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('scientific_name', 'description')


@register(Breeds)
class BreedsTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Pets)
class PetsTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(PetShots)
class PetShotsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
