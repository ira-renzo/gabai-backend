from django.urls import path

from gabai import views

urlpatterns = [
    path("", views.faqs)
]