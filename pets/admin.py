from django.contrib import admin

# Register your models here.
from .models import Category, Pets, PetShots, Breeds, ReviewWorkers

admin.site.register(Category)
admin.site.register(PetShots)
admin.site.register(Pets)
admin.site.register(Breeds)
admin.site.register(ReviewWorkers)
