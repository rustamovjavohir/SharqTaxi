from django.urls import path, include
from api.billing.views.payme import (CardCreateApiView, MerchantApiView, PaymeGeneratePayLinkView, VerifyCardApiView,
                                     RemoveCardApiView)

urlpatterns = [
    path('merchant/', MerchantApiView.as_view(), name='payme_merchant'),
    path('generate-link/', PaymeGeneratePayLinkView.as_view(), name='payme_generate_link'),
    path('card/create/', CardCreateApiView.as_view(), name='payme_card_create'),
    path('card/verify/', VerifyCardApiView.as_view(), name='payme_card_verify'),
    path('card/remove/', RemoveCardApiView.as_view(), name='payme_card_remove'),
]
