from django.urls import path
from .import views
urlpatterns = [
    path('', views.telephone_diary, name='telephone_diary'),
    path('add', views.add_phone_number, name='add_contact'),
    path('edit/<int:pk>/', views.edit_phone_number, name='edit_contact'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.signout, name='logout'),
]