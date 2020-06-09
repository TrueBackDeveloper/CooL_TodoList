from django.urls import path
from . import views

app_name = 'Todo_List'

urlpatterns = [
    path('', views.index, name='index'),
    path('download_all/', views.download_all_json, name="download_all"),
    path('logout/', views.user_logout, name="logout"),
    path('signup/', views.MyRegisterFormView.as_view(), name="signup"),
    path('login/', views.LoginFormView.as_view(), name="login"),

    path('<int:sheet_id>/<int:note_id>/change_status/', views.change_status, name='change_status'),
    path('<int:sheet_id>/<int:note_id>/note_delete/', views.note_delete, name='note_delete'),
    path('<int:sheet_id>/<int:note_id>/note_edit/', views.note_edit, name='note_edit'),
    path('<int:sheet_id>/sheet_delete/', views.sheet_delete, name='sheet_delete'),
    path('<int:sheet_id>/sheet_edit/', views.sheet_edit, name='sheet_edit'),
    path('create_sheet/', views.create_sheet, name='create_sheet'),
    path('<int:sheet_id>/', views.detail, name='detail'),
    path('<int:sheet_id>/create_note/', views.create_note, name='create_note'),

    path('<int:sheet_id>/<int:note_id>/copy_note/', views.copy_note, name='copy_note'),
    path('<int:sheet_id>/paste_note/', views.paste_note, name='paste_note'),

    path('<int:sheet_id>/download_json/', views.download_json, name='download_json'),

]
