from django.urls import path
from .import views
from .views import Index, Signup, Login, Cart
urlpatterns = [
    path('', Index.as_view(), name='product'),
    path('signup', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    # path('cart/', views.cart, name='cart'),
    path('store/', views.store, name='store'),
     path('cart/', Cart.as_view(), name='cart'),
    # path('store/', views.store, name='store'),

]
