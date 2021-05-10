from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.get_page, name="details"),
    path("help/", views.help, name="help"),
    path("new/", views.create_entry, name="new"),
    path("update/<str:title>/", views.update_entry, name="edit"),
    path("random/", views.random_page, name="random"),
    path("search/", views.get_search_query, name="results")
]