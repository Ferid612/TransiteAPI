from django.urls import path
from . import views,custom_logic

urlpatterns = [
    path('testing/', views.testing),
    
    path('login/', custom_logic.login),
    # path('get_user/', custom_logic.get_user),
    path('check_user/', custom_logic.check_user),
    path('download_csv/',views.download_csv),
    
    path('get_table/', views.get_table),
    path('upload_sql_table/', custom_logic.upload_sql_table),
    path('delete_row_from_table/', views.delete_row_from_table),
    path('delete_row_from_table_with_id/', views.delete_row_from_table_with_id),
    
    path('edit_row_at_table/', views.edit_row_at_table),
    path('add_row_to_table/', views.add_row_to_table),
    
    
]