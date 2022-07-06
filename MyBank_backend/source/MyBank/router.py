from email.mime import base
from rest_framework.routers import DefaultRouter
from user.views import UserViewSet
from transaction.views import BalanceViewSet, TransactionViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(f'bl', BalanceViewSet, basename='balance')
router.register(r'ts', TransactionViewSet, basename='transaction')
urlpatterns = router.urls