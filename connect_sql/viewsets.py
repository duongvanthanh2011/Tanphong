from rest_framework import mixins, viewsets

from .models import *
from .serializers import *

class GiaSanPhamGenericViewSet(viewsets.ModelViewSet):
    queryset = Sanpham.objects.prefetch_related('sanphamnguyenlieu_set__id_nguyenlieu')
    serializer_class = SanPhamSerializer