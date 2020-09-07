from django.contrib import admin

# Register your models here.
from .models import Category, Pets, PetShots, Breeds, ReviewWorkers


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "scientific_name", "url")
    list_display_links = ("scientific_name", )


class ReviewInline(admin.TabularInline):
    model = ReviewWorkers
    extra = 1
    readonly_fields = ("name", "email")


@admin.register(Pets)
class PetsAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "url", "draft")
    list_filter = ("category", "date_in_shelter")
    search_fields = ("name", "category__scientific_name")
    inlines = [ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft", )
    fieldsets = (
        (None, {
            "fields": (("name", "photo"), )
        }),
        (None, {
            "fields": ("breed", )
        }),
        ('Описание', {
            "classes": ('collapse', ),
            "fields": ("description", )
        }),
        (None, {
            "fields": (("age", "date_in_shelter"), )
        }),
        (None, {
            "fields": ("category", )
        }),
        ("Опции", {
            "fields": (("url", "draft"), )
        }),

    )
    # fields = (("breed", ), )


@admin.register(ReviewWorkers)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "pet", "id")
    readonly_fields = ("name", "email")


@admin.register(PetShots)
class PetShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "image", "pet")


@admin.register(Breeds)
class BreedsAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "url")

