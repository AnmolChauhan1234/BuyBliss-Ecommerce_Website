from . import views
from django.urls import path

urlpatterns = [
    path('', views.index,name="ShopHome"),
    path('about/', views.about,name="AboutUs"),
    path('contact/', views.contact,name="ContatcUs"),
    path('tracker/', views.tracker,name="TrackingStatus"),
    path('search/', views.search,name="Search"),
    path('products/<int:myid>', views.productView,name="ProductView"),
    path('checkout/', views.checkout,name="Checkout"),
    path('view_cart/', views.view_cart,name="Cart"),
    path('signup/', views.handleSignup,name="handleSignup"),
    path('login/', views.handleLogin,name="handleLogin"),
    path('logout/', views.handleLogout,name="handleLogout"),
    path('update_cartItem/', views.update_cartItem,name="update_cartItem"),
    path('updateCart/', views.updateCart,name="updateCart"),
    path('decreaseQuantity/', views.decreaseQuantity,name="decreaseQuantity"),
    path('increaseQuantity/', views.increaseQuantity,name="increaseQuantity"),
]