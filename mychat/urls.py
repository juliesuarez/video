from django.urls import path
from . import views
# from .views import generate_agora_key

urlpatterns = [
    path('mind/', views.mind),
    path('room/', views.room),
    path('get_token/', views.getToken),

    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
    # path('generate_agora_key/', generate_agora_key, name='generate_agora_key')
]