from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginReg),
    path('registration', views.registration),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('cancel', views.cancel),
    path('trips/new', views.tripsnew),
    path('create', views.createtrip),
    path('<int:trip_id>/delete', views.delete),
    path('trips/edit/<int:trip_id>', views.edittrip),
    path('trips/<int:trip_id>/update', views.update),
    path('trips/<int:trip_id>/', views.tripdetails),
]