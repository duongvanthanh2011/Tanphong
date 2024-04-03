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

from datetime import datetime



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


class DonHangAPIView(APIView):
    def convert_data_request(self, request):
        choice_chiphi = request.data.get('chiphi') + request.data.get('packaging')
        chiphi = Chiphi.objects.filter(id_chiphi__in = choice_chiphi)
        gia_chiphi = sum([obj.gia for obj in chiphi])/24500

        choice_sanpham = request.data.get('listProduct')
        sanpham = Giasanpham.objects.filter(id_sanpham__in = [sp['idProduct'] for sp in choice_sanpham])

        id_next_donhang = self.get_next_id_donhang()

        chitietdonhang_data = [
            {
                "id_donhang": id_next_donhang,
                "id_sanpham": sanpham[index].id_sanpham,
                "trongluongnet_kg_field": sanpham[index].Soluongchai_thung * sanpham[index].Trongluong * choice_sanpham[index]['quantity'],
                "trongluonggross_kg_field": None,
                "trongluongnet_chai_kg_field": sanpham[index].Trongluong,
                "soluongthung": choice_sanpham[index]['quantity'],
                "giasanpham_kg": (sanpham[index].Gia + gia_chiphi)/sanpham[index].Trongluong,
                "soluongchai": choice_sanpham[index]['quantity'] * sanpham[index].Soluongchai_thung,
                "trongluongnet_thung_kg_field": sanpham[index].Soluongchai_thung * sanpham[index].Trongluong,
                "trongluonggross_thung_kg_field": None,
                "tonggiasanpham": (sanpham[index].Gia + gia_chiphi)*choice_sanpham[index]['quantity'] * sanpham[index].Soluongchai_thung
            }
            for index in range(len(sanpham))
        ]
        donhang_data = {
            'id_donhang': id_next_donhang,
            'ngay': datetime.now(),
            'chuthich': None,
            'contractno': request.data.get('contract'),
            'shippingline': request.data.get('shippingLine'),
            'shippedper': request.data.get('shippingLine'),
            'portofloading': request.data.get('portOfLoading'),
            'placeofdelivery': request.data.get('placeOfDelivery'),
            'sailingon': request.data.get('sailingOn'),
            'billofladingno': request.data.get('billOfLadingNo'),
            'container_sealno': request.data.get('containerSealNo'),
            'tongsoluong': sum(item['trongluongnet_kg_field'] for item in chitietdonhang_data),
            'tonggia': sum(item['tonggiasanpham'] for item in chitietdonhang_data),
            'donvigiatien': 'USD',
            'bookingno': request.data.get('bookingOn'),
            'id_khachhang': request.data.get('customer'),
        }

        return {
            "donhang": donhang_data,
            "chitietdonhang": chitietdonhang_data
        }
     
    def get_next_id_donhang(self):
        next_id = Donhang.objects.latest('id_donhang').id_donhang
        while Donhang.objects.filter(id_donhang = next_id).exists():
            next_id += 1
        return next_id

    def post(self, request, *args, **kwargs):
        data_request = self.convert_data_request(request)

        serializers_donhang = DonHangSerializer(data = data_request['donhang'])
        if serializers_donhang.is_valid():
            serializers_donhang.save()
        
            serializers_chitietdonhang= ChiTietDonHangSerializer(data = data_request['chitietdonhang'], many = True)
            if serializers_chitietdonhang.is_valid():
                serializers_chitietdonhang.save()
                return Response({
                    "DonHang": serializers_donhang.data,
                    "ChiTietDonHang": serializers_chitietdonhang.data
                })
            
        HttpResponse("False")      


class SanPhamListCreateAPIView(generics.ListAPIView):
    queryset = Sanpham.objects.prefetch_related('sanphamnguyenlieu_set__id_nguyenlieu')
    serializer_class = SanPhamSerializer


class SanPhamRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Sanpham.objects.all()
    serializer_class = SanPhamSerializer


class KhachhangListView(generics.ListAPIView):
    serializer_class = KhachHangSerializer

    def get_queryset(self):
        id_khachhang_list = self.request.data.get('id_khachhang_list', [])
        return Khachhang.objects.filter(id_khachhang__in=id_khachhang_list)



# class CongThucListCreateAPIView(generics.ListCreateAPIView):
#     queryset = San.objects.all()
#     serializer_class = CongThucSerializer