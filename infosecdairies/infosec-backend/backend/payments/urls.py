from django.urls import path

from .views import create_order, verify_payment, my_purchases, razorpay_webhook, get_pricing


urlpatterns = [
    path("create-order/", create_order, name="payments-create-order"),
    path("verify/", verify_payment, name="payments-verify"),
    path("my-purchases/", my_purchases, name="payments-my-purchases"),
    path("webhook/", razorpay_webhook, name="payments-webhook"),
    path("pricing/", get_pricing, name="payments-pricing"),
]
