from django.urls import path

from app.views import create_news_view, list_news_view, get_news_view

urlpatterns = [
    path("news/create", create_news_view),
    path("news/list", list_news_view),
    path("news/<str:news_id>", get_news_view),
]