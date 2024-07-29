from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('view_data/', views.view_data, name='view_data'),
    path('mouse_data/', views.mouse_data, name='mouse_data'),
    path('capture_image/', views.capture_image, name='capture_image'),
]