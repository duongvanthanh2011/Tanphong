from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.db.models import Count, CharField
from django.db.models.functions import Cast
from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins

from collections import defaultdict

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
        trongluong_dongthung = sum([obj.trongluong for obj in chiphi.filter(id_loaichiphi = 6, trongluong__isnull=False)])/1000

        trongluong_sailech = request.data.get("weightDifference")

        choice_sanpham = request.data.get('listProduct')

        id_list = [sp['idProduct'] for sp in choice_sanpham]
        sanpham = Sanpham.objects.filter(id_sanpham__in=id_list)        
        sanpham = sorted(sanpham, key=lambda x: id_list.index(x.id_sanpham))
        print([i.gia for i in sanpham])

        id_next_donhang = self.get_next_id_donhang()

        chitietdonhang_data = [
            {   
                "id_donhang": id_next_donhang,
                "id_sanpham": sp.id_sanpham,
                "trongluongnet_kg_field": sp.soluongchai_thung * sp.trongluong * choice_sanpham[index]['quantity'], #tổng trọng lượng net
                "trongluonggross_kg_field": round((sp.soluongchai_thung * (sp.trongluong + trongluong_sailech + trongluong_dongchai) + trongluong_dongthung) * choice_sanpham[index]['quantity'],2),#tổng trọng lượng gross
                "trongluongnet_chai_kg_field": sp.trongluong,
                "soluongthung": choice_sanpham[index]['quantity'],
                "giasanpham_kg": (sp.gia + gia_chiphi)/sp.trongluong,
                "soluongchai": choice_sanpham[index]['quantity'] * sp.soluongchai_thung,
                "trongluongnet_thung_kg_field": sp.soluongchai_thung * (sp.trongluong + trongluong_sailech), #trọng lượng net/thùng
                "trongluonggross_thung_kg_field": round(sp.soluongchai_thung * (sp.trongluong + trongluong_sailech + trongluong_dongchai) + trongluong_dongthung,2),#trong lượng gross/thùng
                "tonggiasanpham": (sp.gia + gia_chiphi) * choice_sanpham[index]['quantity'] * sp.soluongchai_thung
            }
            for index, sp in enumerate(sanpham)
        ]

        print([i['giasanpham_kg']*i['trongluongnet_chai_kg_field'] for i in chitietdonhang_data])

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
        try:
            next_id = Donhang.objects.latest('id_donhang').id_donhang
        except:
            next_id = 0
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

                backward_info = self.get_backward_info(data_request['donhang'], data_request['chitietdonhang'])
                return Response({
                    "DonHang": serializers_donhang.data,
                    "ChiTietDonHang": serializers_chitietdonhang.data,
                    "BackwardInfo": backward_info
                })
            return Response(serializers_chitietdonhang.errors)

        return Response(serializers_donhang.errors)
    

    def get_backward_info(self, donhang_data, chitietdonhang_data):
        backward_info = []
        total_weight_by_material = {} 

        for chitiet in chitietdonhang_data:
            sanpham = Sanpham.objects.get(id_sanpham=chitiet['id_sanpham'])
            
            # Lấy thông tin nguyên liệu từ bảng SanphamNguyenlieu
            nguyenlieu_info = SanphamNguyenlieu.objects.filter(
                id_sanpham=sanpham.id_sanpham
            ).annotate(
                ten_nguyenlieu=F('id_nguyenlieu'),
                phan_tram=F('phantramtrongluong')
            ).values('ten_nguyenlieu', 'phan_tram')

            # Tính trọng lượng của từng nguyên liệu cho sản phẩm
            materials_weight = {}
            for nguyenlieu in nguyenlieu_info:
                material_id = nguyenlieu['ten_nguyenlieu']
                percentage = nguyenlieu['phan_tram']
                weight = chitiet['trongluongnet_kg_field'] * (percentage / 100)
                
                # Lấy tên nguyên liệu từ bảng Nguyenlieu
                material = Nguyenlieu.objects.get(id_nguyenlieu=material_id)
                material_name = material.ten

                if material_id in materials_weight:
                    materials_weight[material_id]['trongluong'] += weight
                else:
                    materials_weight[material_id] = {
                        'id_nguyenlieu': material_id,
                        'ten_nguyenlieu': material_name,
                        'trongluong': weight,
                        'phan_tram': percentage
                    }

                # Cộng tổng trọng lượng của nguyên liệu
                if material_id in total_weight_by_material:
                    total_weight_by_material[material_id]['trongluong']  += weight
                else:
                    total_weight_by_material[material_id] = {
                    'id_nguyenlieu': material_id,
                    'ten_nguyenlieu': material_name,
                    'trongluong': weight
                }
            backward_info.append({
                'ten_sanpham': sanpham.ten,
                'trongluong_net': chitiet['trongluongnet_kg_field'],
                'nguyen_lieu': [
                {
                    'id_nguyenlieu': info['id_nguyenlieu'],
                    'ten_nguyenlieu': info['ten_nguyenlieu'],
                    'trongluong': info['trongluong'],
                    'phan_tram': info['phan_tram']
                }
                for info in materials_weight.values()
            ]
            })

        return {
            "backward_info": backward_info,
            "total_weight_by_material": total_weight_by_material
        }
    
