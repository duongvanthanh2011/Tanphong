from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import *



class GiaSanPhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Giasanpham
        fields = "__all__"
    
class KhachHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Khachhang
        fields = '__all__'

class ChiTietDonHangSerializer(serializers.ModelSerializer):
    ten_sanpham = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Chitietdonhang
        fields = "__all__"
    
    def get_ten_sanpham(self, obj):
        return obj.id_sanpham.ten

class DonHangSerializer(serializers.ModelSerializer):
    khachhang = KhachHangSerializer(read_only = True, source = 'id_khachhang')
    class Meta:
        model = Donhang
        fields = "__all__"


class NguyenlieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nguyenlieu
        fields = ['id_nguyenlieu', 'ten', 'gia']

class SanphamNguyenlieuSerializer(serializers.ModelSerializer):
    nguyenlieu = NguyenlieuSerializer(source='id_nguyenlieu')  # Use source to access the related Nguyenlieu object

    class Meta:
        model = SanphamNguyenlieu
        fields = ['nguyenlieu', 'trongluong']

class ChiPhiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chiphi
        fields = '__all__'

class SanPhamSerializer(serializers.ModelSerializer):
    # sanphamnguyenlieu_set = SanphamNguyenlieuSerializer(many=True)
    # gia_final = serializers.SerializerMethodField()
    # trong_luong_final = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Sanpham
        fields = "__all__"
        # read_only_fields  = ['sanphamnguyenlieu_set', 'gia_final']

    # def get_trong_luong_final(self, obj):
    #     trongluong = 0
    #     for nguyenlieu in obj.sanphamnguyenlieu_set.all():
    #         trongluong +=  nguyenlieu.trongluong
    #     return trongluong

    # def get_gia_final(self,obj):
    #     gia = 0
    #     for nguyenlieu in obj.sanphamnguyenlieu_set.all():
    #         gia += nguyenlieu.id_nguyenlieu.gia * nguyenlieu.trongluong
    #     return gia/24500
    
    # def get_url(self, obj):
    #     request = self.context.get('request')
    #     if request is None:
    #         return None
    #     return reverse('sanpham-retrieve', request=request, kwargs={'pk':obj.pk})
    