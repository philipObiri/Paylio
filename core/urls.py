from django.urls import path
from core import views
# from core import views, transfer, transaction, payment_request, credit_card


app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
]

