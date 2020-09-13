from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Pets, Category, Breeds, Rating
from .forms import ReviewForm, RatingForm


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
    paginate_by = 3


class PetDetailView(BreedYear, DetailView):
    """Полное описание питомца"""
    model = Pets
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewForm()
        return context


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
    paginate_by = 3

    def get_queryset(self):
        queryset = Pets.objects.filter(
            Q(age__in=self.request.GET.getlist("age")) |
            Q(breed__in=self.request.GET.getlist("breed"))
        ).distinct()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["age"] = ''.join(f"age={x}&" for x in self.request.GET.getlist("age"))
        context["breed"] = ''.join(f"breed={x}&" for x in self.request.GET.getlist("breed"))
        return context


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


class AddStarRating(View):
    """Добавление рейтинга"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                pet_id=int(request.POST.get("pet")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Поиск питомцев"""
    paginate_by = 3

    def get_queryset(self):
        return Pets.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}'
        return context
