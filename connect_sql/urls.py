from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('sanpham/', views.SanPhamAPIView.as_view(), name = 'sanpham-list'),
    path('donhang/', views.DonHangAPIView.as_view(), name = 'donhang'),
]