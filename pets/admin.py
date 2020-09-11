from django import forms
from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from .models import Category, Pets, PetShots, Breeds, ReviewWorkers


from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Pets
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "scientific_name", "url")
    list_display_links = ("scientific_name", )


class ReviewInline(admin.TabularInline):
    model = ReviewWorkers
    extra = 1
    readonly_fields = ("name", "email")


class PetShotsInline(admin.TabularInline):
    model = PetShots
    extra = 1
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="65" height="80"')
    get_image.short_description = "Фото"


@admin.register(Pets)
class PetsAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "url", "draft")
    list_filter = ("category", "date_in_shelter")
    search_fields = ("name", "category__scientific_name")
    inlines = [PetShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft", )
    actions = ["publish", "unpublish"]
    form = PostAdminForm
    readonly_fields = ("get_image", )
    fieldsets = (
        (None, {
            "fields": ("name", ("photo", "get_image"), )
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

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="170" height="170"')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ("change", )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ("change",)

    get_image.short_description = "Фото"


@admin.register(ReviewWorkers)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "pet", "id")
    readonly_fields = ("name", "email", )


@admin.register(PetShots)
class PetShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "image", "pet", "get_image")
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="65" height="80"')
    get_image.short_description = "Фото"


@admin.register(Breeds)
class BreedsAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "url")


admin.site.site_title = 'Django Pets'
admin.site.site_header = 'Django Pets'
