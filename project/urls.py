from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about_us, name='about'),
    path('menu', views.menu_cat, name='menu'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('register', views.sign_up_page, name='register'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('product', views.products, name='product'),
    path('update_Item/', views.updateItems, name='update_Item'),
    path('process_order/', views.process_order, name='process_order'),
]
