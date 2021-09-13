from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:entry>', views.entry, name="entry"),
    path('search', views.search, name="search"),
    path('add', views.add, name='add'),
    path("edit",views.edit, name='edit'),
    path("save",views.save, name='save'),
    path("randomEntry",views.randomEntry, name='randomEntry')
    
]
