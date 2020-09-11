from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Pets, Category, Breeds
from .forms import ReviewForm


class BreedYear:
    """Породы и года поступления в приют"""

    def get_breeds(self):
        return Breeds.objects.filter()

    def get_ages(self):
        return Pets.objects.filter(draft=False).values("age")


class PetsView(BreedYear, ListView):
    """Список питомцев"""
    model = Pets
    queryset = Pets.objects.filter(draft=False)


class PetDetailView(BreedYear, DetailView):
    """Полное описание питомца"""
    model = Pets
    slug_field = "url"


class AddReview(View):
    """Комментарий сотрудника или гостя"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        pet = Pets.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.pet = pet
            form.save()
        return redirect(pet.get_absolute_url())


class FilterPetsView(BreedYear, ListView):
    """Фильтр питомцев"""

    def get_queryset(self):
        queryset = Pets.objects.filter(
            Q(age__in=self.request.GET.getlist("age")) |
            Q(breed__in=self.request.GET.getlist("breed"))
        )

        return queryset


class JsonFilterPetsView(ListView):
    """Фильтр питомцев json"""
    def get_queryset(self):
        queryset = Pets.objects.filter(
            Q(age__in=self.request.GET.getlist("age")) |
            Q(breed__in=self.request.GET.getlist("breed"))
        ).distinct().values("name", "description", "url", "photo")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"pets": queryset}, safe=False)
