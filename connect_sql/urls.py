from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('sanpham/', views.SanPhamAPIView.as_view(), name =  'sanpham-list'),
    path('sanpham/<str:pk>', views.SanPhamRetrieveAPIView.as_view(), name =  'sanpham-retrieve'),
    path('test_kh/', views.KhachhangListView.as_view()),
    path('donhang/', views.DonHangGenericAPIView.as_view()),
    path('donhang/<int:pk>', views.DonHangGenericAPIView.as_view())
]