from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("destinations/", views.destinations, name="destinations"),
    path("users/new/", views.sign_up, name="sign_up"),
    path("users/", views.create_user, name="create_user"),
    path("sessions/new/", views.sign_in, name="sign_in"),
    path("sessions/", views.validate_user, name="validate_user"),
    path("sessions/destroy/", views.logout, name="logout"),
    path("destinations/new/", views.new_destination, name="new_destination"),
    path("destinations/<int:id>/", views.edit_destination, name="edit_destination"),
    path("destinations/<int:id>/destroy/", views.delete_destination, name="delete_destination")
]