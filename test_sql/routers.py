from rest_framework.routers import DefaultRouter

from connect_sql.viewsets import GiaSanPhamGenericViewSet

router = DefaultRouter()
router.register('sanpham', GiaSanPhamGenericViewSet, basename='sanpham-viewset')

urlpatterns = router.urls

# urlpatterns = [
#     path("<str:pk>")
# ]