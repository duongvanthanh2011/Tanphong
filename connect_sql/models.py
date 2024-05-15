from django.db import models



class Sanpham(models.Model):
    id_sanpham = models.CharField(db_column='Id_SanPham', primary_key=True, max_length=1000)  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=1000)  # Field name made lowercase.
    chuthich = models.CharField(db_column='ChuThich', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    gia = models.FloatField(db_column='Gia', blank=True, null=True)  # Field name made lowercase.
    trongluong = models.FloatField(db_column='TrongLuong', blank=True, null=True)  # Field name made lowercase.
    soluongchai_thung = models.BigIntegerField(db_column='SoLuongChai/Thung', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'SanPham'
        
class Chiphi(models.Model):
    id_chiphi = models.CharField(db_column='Id_ChiPhi', primary_key=True, max_length=100)  # Field name made lowercase.
    id_loaichiphi = models.ForeignKey('Loaichiphi', models.DO_NOTHING, db_column='Id_LoaiChiPhi')  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=100, blank=True, null=True)  # Field name made lowercase.
    chuthich = models.CharField(db_column='ChuThich', max_length=100, blank=True, null=True)  # Field name made lowercase.
    gia = models.FloatField(db_column='Gia', blank=True, null=True)  # Field name made lowercase.
    trongluong = models.FloatField(db_column='TrongLuong', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ChiPhi'


class Chitietdonhang(models.Model):
    id_chitietdonhang = models.BigAutoField(db_column='id_ChiTietDonHang', primary_key=True)  # Field name made lowercase.
    id_donhang = models.ForeignKey('Donhang', models.DO_NOTHING, db_column='Id_DonHang', blank=True, null=True)  # Field name made lowercase.
    id_sanpham = models.ForeignKey('Sanpham', models.DO_NOTHING, db_column='Id_SanPham', blank=True, null=True)  # Field name made lowercase.
    trongluongnet_kg_field = models.FloatField(db_column='TrongLuongNet(KG)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    trongluonggross_kg_field = models.FloatField(db_column='TrongLuongGross(KG)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    trongluongnet_chai_kg_field = models.FloatField(db_column='TrongLuongNet/Chai(KG)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    soluongthung = models.FloatField(db_column='SoLuongThung', blank=True, null=True)  # Field name made lowercase.
    giasanpham_kg = models.FloatField(db_column='GiaSanPham/KG', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    soluongchai = models.BigIntegerField(db_column='SoLuongChai', blank=True, null=True)  # Field name made lowercase.
    trongluongnet_thung_kg_field = models.FloatField(db_column='TrongLuongNet/Thung(KG)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    trongluonggross_thung_kg_field = models.FloatField(db_column='TrongLuongGross/Thung(KG)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    tonggiasanpham = models.FloatField(db_column='TongGiaSanPham', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ChiTietDonhang'


class Donhang(models.Model):
    id_donhang = models.BigIntegerField(db_column='id_DonHang', primary_key=True)  # Field name made lowercase.
    ngaytao = models.DateTimeField(db_column='NgayTao', blank=True, null=True)  # Field name made lowercase.
    id_khachhang = models.ForeignKey('Khachhang', models.DO_NOTHING, db_column='id_KhachHang', blank=True, null=True)  # Field name made lowercase.   
    chuthich = models.CharField(db_column='ChuThich', max_length=100, blank=True, null=True)  # Field name made lowercase.
    contractno = models.CharField(db_column='ContractNo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    shippingline = models.CharField(db_column='ShippingLine', max_length=100, blank=True, null=True)  # Field name made lowercase.
    shippedper = models.CharField(db_column='ShippedPer', max_length=100, blank=True, null=True)  # Field name made lowercase.
    portofloading = models.CharField(db_column='PortOfLoading', max_length=100, blank=True, null=True)  # Field name made lowercase.
    placeofdelivery = models.CharField(db_column='PlaceOfDelivery', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sailingon = models.CharField(db_column='SailingOn', max_length=100, blank=True, null=True)  # Field name made lowercase.
    billofladingno = models.CharField(db_column='BillOfLadingNo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    container_sealno = models.CharField(db_column='Container/SealNo', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tongsoluong = models.FloatField(db_column='TongSoLuong', blank=True, null=True)  # Field name made lowercase.
    tonggia = models.FloatField(db_column='TongGia', blank=True, null=True)  # Field name made lowercase.
    donvigiatien = models.CharField(db_column='DonViGiaTien', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bookingno = models.CharField(db_column='BookingNo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    no = models.CharField(db_column='No', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DonHang'


class Khachhang(models.Model):
    id_khachhang = models.CharField(db_column='id_KhachHang', primary_key=True, max_length=100)  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=100, blank=True, null=True)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=100, blank=True, null=True)  # Field name made lowercase.
    quocgia = models.CharField(db_column='QuocGia', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hoatdong = models.BigIntegerField(db_column='HoatDong', blank=True, null=True)  # Field name made lowercase.
    sdt = models.TextField(db_column='SDT', blank=True, null=True)  # Field name made lowercase.
    fax = models.TextField(db_column='FAX', blank=True, null=True)  # Field name made lowercase.
    zipcode = models.TextField(db_column='ZipCode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KhachHang'


class Loaichiphi(models.Model):
    id_loaichiphi = models.CharField(db_column='Id_LoaiChiPhi', primary_key=True, max_length=100)  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=100)  # Field name made lowercase.
    chuthich = models.CharField(db_column='ChuThich', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LoaiChiPhi'


class Loainguyenlieu(models.Model):
    id_loainguyenlieu = models.CharField(db_column='Id_LoaiNguyenLieu', primary_key=True, max_length=100)  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=100)  # Field name made lowercase.
    chuthich = models.CharField(db_column='ChuThich', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LoaiNguyenLieu'


class Nguyenlieu(models.Model):
    id_nguyenlieu = models.CharField(db_column='Id_NguyenLieu', primary_key=True, max_length=100)  # Field name made lowercase.
    id_loainguyenlieu = models.ForeignKey(Loainguyenlieu, models.DO_NOTHING, db_column='Id_LoaiNguyenLieu')  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=100, blank=True, null=True)  # Field name made lowercase.
    gia = models.FloatField(db_column='Gia', blank=True, null=True)  # Field name made lowercase.
    xuatxu = models.CharField(db_column='XuatXu', max_length=100, blank=True, null=True)  # Field name made lowercase.
    chuthich = models.CharField(db_column='ChuThich', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NguyenLieu'



class SanphamNguyenlieu(models.Model):
    id = models.BigIntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    id_sanpham = models.ForeignKey(Sanpham, models.DO_NOTHING, db_column='Id_SanPham', blank=True, null=True)  # Field name made lowercase.
    id_nguyenlieu = models.CharField(db_column='Id_NguyenLieu', max_length=100, blank=True, null=True)  # Field name made lowercase.
    trongluong = models.FloatField(db_column='TrongLuong', blank=True, null=True)  # Field name made lowercase.
    phantramtrongluong = models.FloatField(db_column='PhanTramTrongLuong', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SanPham_NguyenLieu'


class SanphamOld(models.Model):
    id_sanpham_old = models.CharField(db_column='Id_SanPham_Old', primary_key=True, max_length=100)  # Field name made lowercase.
    id_sanpham = models.ForeignKey(Sanpham, models.DO_NOTHING, db_column='Id_SanPham')  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=100, blank=True, null=True)  # Field name made lowercase.
    xuatxu = models.CharField(db_column='XuatXu', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SanPham_Old'


class TuybienChiphi(models.Model):
    id_khachhang = models.ForeignKey(Khachhang, models.DO_NOTHING, db_column='id_KhachHang')  # Field name made lowercase.
    id_chiphi = models.ForeignKey(Chiphi, models.DO_NOTHING, db_column='id_ChiPhi', blank=True, null=True)  # Field name made lowercase.
    id_tuybien_chiphi = models.BigIntegerField(db_column='Id_Tuybien_Chiphi', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TuyBien_ChiPhi'