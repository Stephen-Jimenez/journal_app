from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_reg),
    path('register', views.register),
    path('landing', views.landing),
    path('logout', views.logout),
    path('login', views.login),
    path('create_journal_entry', views.create_entry),
    path('my_entries/<int:current_user_id>', views.my_entries),
    path('view_entry/<int:entry_id>', views.view_entry),
    path('delete/<int:entry_id>', views.delete),
    path('delete_entry/<int:entry_id>', views.delete_entry),
    path('edit_journal_entry/<int:entry_id>', views.edit_entry),
    path('edit_user_info/<int:current_user_id>', views.edit_user_info),
    path('edit_user_info_complete/<int:current_user_id>', views.edit_user_info_complete)
]