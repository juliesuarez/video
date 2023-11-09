from django.urls import path, include
from .views import InboxView, UserListsView, MessagesListView, signup
from django.contrib.auth import views as auth_views

from . import views
from .feeds import AtomSiteNewsFeed, LatestPostsFeed
from . views import Login
from chat.view import *
from .views import CreateAppointmentView, UserAppointmentsView
from .views import edit_appointment
app_name = 'chat'


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', MessagesListView.as_view(), name='message_list'),
    path('meet/', UserListsView.as_view(), name='users_list'),
    path('inbox/<str:username>/', InboxView.as_view(), name='inbox'),
    path('login/', Login, name ='login'),
    #path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='chat:message_list'), name='logout'),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),

    path("summernote/", include("django_summernote.urls")),
    path('editor/', include('django_summernote.urls')),
    path('thrpy/', teachers.QuizListView, name='QuizListView'),
    path('organization/', organization.QuizListView, name='QuizListView'),

    path('posts/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/update/', views.post_update, name='post_update'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),

    path('patients/', views.patients, name='patients'),
    path('create/', CreateAppointmentView.as_view(), name='create_appointment'),
    path('user_appointments/', UserAppointmentsView.as_view(), name='user_appointments'),
    path('available-therapists/', views.available_therapists, name='available_therapists'),
    path('create-appointment-slot/', views.create_appointment_slot, name='create-appointment-slot'),
    path('edit-appointment-slot/<int:slot_id>/', views.edit_appointment_slot, name='edit_appointment_slot'),
    path('get_available_times/<int:therapist_id>/', CreateAppointmentView.as_view(), name='get_available_times'),
    path('update-appointment-status/', views.update_appointment_status, name='update-appointment-status'),
    path('finished-appointments/', views.finished_appointments, name='finished_appointments'),
    path('appointments/<int:pk>/edit/', edit_appointment, name='edit_appointment'),
    path('profile/', views.user_profile, name='user_profile'),
    path('view-appointment-slots/', views.view_appointment_slots, name='view_appointment_slots'),
]
