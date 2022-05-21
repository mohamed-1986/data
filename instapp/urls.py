from django.urls import path


from .views import *

from . import views


urlpatterns = [
    path('', views.HomeView, name = 'home'),
    path('search/', Search.as_view(), name= 'search'),
    path('tag/<slug>/' , Tag.as_view() , name='tag_url'),
    path('inst/add/', views.add_ins , name= 'add_inst'),
    path('tag/<slug>/add-manual/', views.add_manual_to_inst , name='add_manual'),
    # path('account/logout/', views.logout_view , name= 'logout_url'),
    # path('account/login/', views.login_page , name = 'login_url'),
    # path('login/' , views.login_view , name='login'),
]
