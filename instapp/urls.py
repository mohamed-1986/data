from django.urls import path


from .views import *

from . import views


urlpatterns = [
    path('', views.HomeView, name = 'home'),
    path('search/', Search.as_view(), name= 'search'),
    path('tag/<slug>/' , Tag.as_view() , name='tag_url'),
    path('inst/add/', views.add_ins , name= 'add_inst'),
    path('tag/<slug>/add-manual/', views.add_manual_to_inst , name='add_manual'),
    path('pid/' , views.pid_unit_filtered , name = 'pid_url' ),
    path('pid/<unit>', views.pid_pk, name = 'pid_pk_url'),
    path('manuals/', views.category_of_manual, name='manual_categories_url'),
    path('manuals/<cat>', views.manual_pk, name = 'man_pk_url'),
]
