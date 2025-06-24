from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('waiter/', views.waiter_dashboard, name='waiter_dashboard'),
    path('kitchen/', views.kitchen_dashboard, name='kitchen_dashboard'),
    path('add-order/', views.add_order, name='add_order'),
    path('add-account/', views.add_account, name='add_account'),
    path('table/<int:table_id>/', views.table_detail, name='table_detail'),
    path('table/<int:table_id>/add-account/', views.add_account, name='add_account'),
    path('account/<int:account_id>/add-order/', views.add_order, name='add_order'),
]