from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.db.models import Sum, F, ExpressionWrapper, FloatField

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins

from .models import *
from .serializers import *
from pprint import pprint
# Create your views here.

def index(request):
    return HttpResponse("hello world")

# class SanPhamAPI(APIView):
#     def get(self, request):
#         # ORM --------------------------------
#         queryset = Giasanpham.objects.values('id_sanpham', 'Ten', 'Trongluong', 'Gia')
#         serializer = GiaSanPhamSerializer(queryset, many = True, )
        # return Response(serializer.data)
    
        # with connection.cursor() as cursor:
        #     cursor.execute('select * from "final_sp_gia"')
        #     rows = cursor.fetchall()
        # data = []
        # for row in rows:
        #     row_dict = {}
        #     for index, column_name in enumerate(cursor.description):
        #         row_dict[column_name[0]] = row[index]
        #     data.append(row_dict)

        # return Response(data)

# class GiaSanPhamListCreateAPIView(generics.ListCreateAPIView):
#     queryset =  Giasanpham.objects.all()
#     serializer_class = GiaSanPhamSerializer
#     # lookup_field = 'id_sanpham'

# class GiaSanPhamRetrieveAPIView(generics.RetrieveAPIView):
#     queryset =  Giasanpham.objects.all()
#     serializer_class = GiaSanPhamSerializer
#     # lookup_field = 'id_sanpham'

class SanPhamAPIView(APIView):
    def get(self, request):
        sanphams = Sanpham.objects.prefetch_related('sanphamnguyenlieu_set__id_nguyenlieu')
        serializers_sanpham = SanPhamSerializer(sanphams, many = True)

        khachhang = Khachhang.objects.all()
        serializer_khachhang = KhachHangSerializer(khachhang, many = True)

        packaging_chiphi = Chiphi.objects.filter(id_loaichiphi =2)
        serializers_packaging = ChiPhiSerializer(packaging_chiphi, many = True)

        chiphi = Chiphi.objects.exclude(id_loaichiphi = 2)
        serializers_chiphi = ChiPhiSerializer(chiphi, many = True)


        return Response({'sanpham':serializers_sanpham.data, 
                         'khachhang':serializer_khachhang.data, 
                         'packagking':serializers_packaging.data, 
                         'chiphi':serializers_chiphi.data})


class SanPhamListCreateAPIView(generics.ListAPIView):
    queryset = Sanpham.objects.prefetch_related('sanphamnguyenlieu_set__id_nguyenlieu')
    serializer_class = SanPhamSerializer


class SanPhamRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Sanpham.objects.all()
    serializer_class = SanPhamSerializer


# class CongThucListCreateAPIView(generics.ListCreateAPIView):
#     queryset = San.objects.all()
#     serializer_class = CongThucSerializer