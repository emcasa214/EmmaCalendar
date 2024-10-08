"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Emma import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome, name = 'welcome' ),
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.loginpage, name = 'login'),
    path('setting/', views.setting, name = 'setting'),
    path ('reset/', views.reset, name = 'reset'),
    path('task_list/', views.task_list, name="task_list"),
    path("calendar/", views.calendar, name="calendar"),
    path('all_task/', views.all_task, name='all_task'), 
    path('add_task/', views.add_task, name='add_task'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
    path('logout/',views.LogoutView, name = 'logout'),
    path('pomodoro/', views.pomodoro_timer, name='pomodoro_timer'),
]
