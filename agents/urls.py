from django.urls import path
from . import views

app_name='agents'

urlpatterns = [
    path('',views.agent_list_view.as_view(),name='agent-list'),
    path('create/',views.agent_create_view.as_view(),name='agent-create'),
    path('<int:pk>/',views.agent_detail_view.as_view(),name='agent-detail'),
    path('<int:pk>/update',views.agent_update_view.as_view(),name='agent-update'),
    path('<int:pk>/delete',views.agent_delete_view.as_view(),name='agent-delete'),
]
