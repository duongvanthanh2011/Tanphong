from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import *


class NguyenlieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nguyenlieu
        fields = ['id_nguyenlieu', 'ten', 'gia']

class SanphamNguyenlieuSerializer(serializers.ModelSerializer):
    nguyenlieu = NguyenlieuSerializer(source='id_nguyenlieu')  # Use source to access the related Nguyenlieu object

    class Meta:
        model = SanphamNguyenlieu
        fields = ['nguyenlieu', 'trongluong']

class SanPhamSerializer(serializers.ModelSerializer):
    sanphamnguyenlieu_set = SanphamNguyenlieuSerializer(many=True)
    gia_final = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Sanpham
        fields = ['url','id_sanpham', 'ten', 'sanphamnguyenlieu_set', 'gia_final']
        read_only_fields  = ['sanphamnguyenlieu_set', 'gia_final']
    
    def get_gia_final(self,obj):
        gia = 0
        for nguyenlieu in obj.sanphamnguyenlieu_set.all():
            gia += nguyenlieu.id_nguyenlieu.gia * nguyenlieu.trongluong
        return gia/24500
    
    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('sanpham-retrieve', request=request, kwargs={'pk':obj.pk})


    
