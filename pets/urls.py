from django.urls import path

from . import views

urlpatterns = [
    path("", views.PetsView.as_view()),
    path("filter/", views.FilterPetsView.as_view(), name="filter"),
    path("json-filter/", views.JsonFilterPetsView.as_view(), name="json_filter"),
    path("<slug:slug>/", views.PetDetailView.as_view(), name="pets_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
]
