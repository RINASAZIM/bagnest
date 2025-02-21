#urls.py
from django.urls import path
from . import views

urlpatterns=[
    path("",views.main,name='main'),
    path('detailsadd/',views.detailsadd,name='detailsadd'),
    path('productdetail/',views.productdetails,name='productdetail'),
    path('viewproduct/',views.vieww,name='viewproduct'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path("cart/", views.view_cart, name="cart"),
    path("update-cart/", views.update_cart, name="update_cart"),
    path('register/',views.register,name="register"),
    path('login/',views.loginn,name='login'),
    path('userlog/',views.userlog,name="userlogs"),
    path("logoutu/",views.logoutuser,name="logout"),
    path("checkout/", views.checkout, name="checkout"),
    path("purchase-history/", views.purchase_history, name="purchase_history"),
    path("download-purchase-history/", views.download_purchase_history, name="download_purchase_history"),
    path('contact/',views.contact,name='contact'),
]
