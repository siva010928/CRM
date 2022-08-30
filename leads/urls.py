from django.urls import path
from . import views

app_name='leads'
urlpatterns = [
    path('',views.lead_list_view.as_view(),name='lead-list'),
    path('<int:pk>/',views.lead_detail_view.as_view(),name='lead-detail'),
    path('<int:pk>/update/',views.lead_update_view.as_view(),name='lead-update'),
    path('<int:pk>/delete/',views.lead_delete_view.as_view(),name='lead-delete'),
    path('<int:pk>/assign_agent/',views.assign_agent_view.as_view(),name='assign-agent'),
    path('<int:pk>/category_update/',views.lead_category_update_view.as_view(),name='lead-update-category'),
    path('create/',views.lead_create_view.as_view(),name='lead-create'),
    path('category/',views.category_list_view.as_view(),name='category-list'),
    path('category/create/',views.category_create_view.as_view(),name='category-create'),
    path('category/<int:pk>/',views.category_detail_view.as_view(),name='category-detail'),
    path('category/<int:pk>/update',views.category_update_view.as_view(),name='category-update'),
    path('category/<int:pk>/delete',views.category_delete_view.as_view(),name='category-delete'),
]
