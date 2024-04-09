from django.contrib import admin
from .models import *

# admin.site.register(Sanpham)
# Register your models here.

@admin.register(Sanpham)
class SanPhamAdmin(admin.ModelAdmin):
    list_display = ("id_sanpham", "ten", "gia", "trongluong", "chuthich", "soluongchai_thung")

@admin.register(SanphamNguyenlieu)
class SanPhamNguyenLieuAdmin(admin.ModelAdmin):
    list_display = ("id", "id_sanpham", "id_nguyenlieu", "trongluong")

@admin.register(Nguyenlieu)
class NguyenLieuAdmin(admin.ModelAdmin):
    list_display = ("id_nguyenlieu", "id_loainguyenlieu", "ten", "gia", "xuatxu", "chuthich")