from django.urls import path

from apps.news.views import create_news_view, list_news_view

urlpatterns = [
    path("create", create_news_view),
    path("list", list_news_view)
]