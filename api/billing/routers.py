from api.billing.views import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('payment', views.UserPaymentViewSet, basename='payment')
router.register('card', views.BankCardViewSet, basename='card')
