from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.error_page , name="wiki_default"),
    path("create/" , views.new_page , name="create"),
    path("search/", views.search , name="search"),
    path("edit/" , views.edit_page, name="edit"),
    path("save_edit/" , views.save_edit , name="save"),
    path("wiki/<slug:slug>/", views.dynamic_look_up , name="entry"),
    path("random/" , views.random_page , name="random")
]
