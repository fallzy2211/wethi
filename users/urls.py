
from .views import create_offer, offer_list, reserve_offer, chat, available_offers, dashboard, filtered_offers, \
    process_payment, custom_logout, signup, register
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, RegisterView

urlpatterns = [
    path('create/', create_offer, name='create_offer'),
    path('offers/', offer_list, name='offer_list'),
    path('register/', register, name='register'),
    path('reserve/<int:offer_id>/', reserve_offer, name='reserve_offer'),
    path('chat/<int:offer_id>/', chat, name='chat'),
    path('available_offers/', available_offers, name='available_offers'),
    path('dashboard/', dashboard, name='dashboard'),
    path('filtered_offers/', filtered_offers, name='filtered_offers'),
    path('process_payment/', process_payment, name='process_payment'),
    path('logout/', custom_logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Ajoute cette ligne
]

