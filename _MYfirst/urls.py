from django.contrib import admin
from django.urls import path, include
from Todo_List import views

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('Todolist/', include('Todo_List.urls')),
    path('admin/', admin.site.urls),

]

