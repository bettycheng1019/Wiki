from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:entry>', views.entry, name="entry"),
    path('search', views.search, name="search"),
    path('add', views.add, name='add'),
    path("editPage",views.editPage, name='editPage'),
    path("saveEdit",views.saveEdit, name='saveEdit'),
    path("randomEntry",views.randomEntry, name='randomEntry')
    
]
