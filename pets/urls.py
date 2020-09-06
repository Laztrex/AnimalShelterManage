from django.urls import path

from . import views

urlpatterns = [
    path("", views.PetsView.as_view()),
    path("<slug:slug>/", views.PetDetailView.as_view(), name="pets_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
]
