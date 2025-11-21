from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("inventory/", views.inventory, name="inventory"),
    path("inventory/add/", views.add_item, name="add_item"),
    path("inventory/<int:pk>/edit/", views.edit_item, name="edit_item"),
]
