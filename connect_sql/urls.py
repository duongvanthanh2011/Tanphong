from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('sanpham/', views.SanPhamListCreateAPIView.as_view(), name =  'sanpham-list'),
    path('sanpham/<str:pk>', views.SanPhamRetrieveAPIView.as_view(), name =  'sanpham-retrieve')
]