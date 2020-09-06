from django.shortcuts import render, redirect

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Pets
from .forms import ReviewForm


class PetsView(ListView):
    """Список питомцев"""
    model = Pets
    queryset = Pets.objects.filter(draft=False)
    # template_name = "pets/pets_list.html"


class PetDetailView(DetailView):
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
            form.pet = pet
            form.save()
        return redirect(pet.get_absolute_url())

