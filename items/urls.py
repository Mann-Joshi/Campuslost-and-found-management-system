from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.FindItLoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('report/', views.report_item, name='report'),
    path('edit/<int:item_id>/', views.edit_item, name='edit'),
    path('delete/<int:item_id>/', views.delete_item, name='delete'),
]
