from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.db.models import Count, CharField
from django.db.models.functions import Cast

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins

from .models import *
from .serializers import *
from pprint import pprint

from datetime import datetime


def index(request):
    return HttpResponse("hello world")


class SanPhamAPIView(APIView):
    def get(self, request):
        sanphams = Sanpham.objects.all()
        serializers_sanpham = SanPhamSerializer(sanphams, many = True)

        khachhang = Khachhang.objects.all()
        serializer_khachhang = KhachHangSerializer(khachhang, many = True)

        packaging_chiphi = Chiphi.objects.filter(id_loaichiphi =2)
        serializers_packaging = ChiPhiSerializer(packaging_chiphi, many = True)

        chiphi = Chiphi.objects.exclude(id_loaichiphi = 2)
        serializers_chiphi = ChiPhiSerializer(chiphi, many = True)


        donhang = Donhang.objects.values(
            "contractno",
            "shippingline",
            "shippedper",
            "portofloading",
            "placeofdelivery"
        ).annotate(
            contractno_count=Count('contractno'),
            shippingline_count=Count('shippingline'),
            shippedper_count=Count('shippedper'),
            portofloading_count=Count('portofloading'),
            placeofdelivery_count=Count('placeofdelivery')
        )

        contractno = donhang.values_list("contractno", flat=True).distinct()
        shippingline = donhang.values_list("shippingline", flat=True).distinct()
        shippedper = donhang.values_list("shippedper", flat=True).distinct()
        portofloading = donhang.values_list("portofloading", flat=True).distinct()
        placeofdelivery = donhang.values_list("placeofdelivery", flat=True).distinct()


        return Response({'sanpham':serializers_sanpham.data, 
                         'khachhang':serializer_khachhang.data, 
                         'packagking':serializers_packaging.data, 
                         'chiphi':serializers_chiphi.data,
                         "contractno": contractno,
                         "shippingline":shippingline,
                         "shippedper":shippedper,
                         "portofloading":portofloading,
                         "placeofdelivery": placeofdelivery})


class DonHangAPIView(APIView):
    def convert_data_request(self, request):
        choice_chiphi = request.data.get('chiphi') + request.data.get('packaging')
        
        chiphi = Chiphi.objects.filter(id_chiphi__in = choice_chiphi)
        gia_chiphi = sum([obj.gia for obj in chiphi])/24500
        
        trongluong_dongchai = sum([obj.trongluong for obj in chiphi.filter(id_loaichiphi = 2, trongluong__isnull=False)])/1000
        print(trongluong_dongchai)
        trongluong_dongthung = sum([obj.trongluong for obj in chiphi.filter(id_loaichiphi = 6, trongluong__isnull=False)])/1000

        trongluong_sailech = request.data.get("weightDifference")

        choice_sanpham = request.data.get('listProduct')

        id_list = [sp['idProduct'] for sp in choice_sanpham]
        sanpham = Sanpham.objects.filter(id_sanpham__in=id_list)        
        sanpham = sorted(sanpham, key=lambda x: id_list.index(x.id_sanpham))

        id_next_donhang = self.get_next_id_donhang()

        chitietdonhang_data = [
            {   
                "id_donhang": id_next_donhang,
                "id_sanpham": sp.id_sanpham,
                "trongluongnet_kg_field": sp.soluongchai_thung * sp.trongluong * choice_sanpham[index]['quantity'],
                "trongluonggross_kg_field": (sp.soluongchai_thung * (sp.trongluong + trongluong_sailech + trongluong_dongchai) + trongluong_dongthung) * choice_sanpham[index]['quantity'],
                "trongluongnet_chai_kg_field": sp.trongluong,
                "soluongthung": choice_sanpham[index]['quantity'],
                "giasanpham_kg": (sp.gia + gia_chiphi)/sp.trongluong,
                "soluongchai": choice_sanpham[index]['quantity'] * sp.soluongchai_thung,
                "trongluongnet_thung_kg_field": sp.soluongchai_thung * (sp.trongluong + trongluong_sailech),
                "trongluonggross_thung_kg_field": sp.soluongchai_thung * (sp.trongluong + trongluong_sailech + trongluong_dongchai) + trongluong_dongthung,
                "tonggiasanpham": (sp.gia + gia_chiphi) * choice_sanpham[index]['quantity'] * sp.soluongchai_thung
            }
            for index, sp in enumerate(sanpham)
        ]

        donhang_data = {
            'id_donhang': id_next_donhang,
            'ngaytao': datetime.now(),
            'chuthich': None,
            'contractno': request.data.get('contract'),
            'shippingline': request.data.get('shippingLine'),
            'shippedper': request.data.get('shippedPer'),
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
            'date': request.data.get('date'),
            'no': request.data.get('no')
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
        
            serializers_chitietdonhang = ChiTietDonHangSerializer(data = data_request['chitietdonhang'], many = True)
            if serializers_chitietdonhang.is_valid():
                serializers_chitietdonhang.save()
                return Response({
                    "DonHang": serializers_donhang.data,
                    "ChiTietDonHang": serializers_chitietdonhang.data
                })
            
        HttpResponse("False")