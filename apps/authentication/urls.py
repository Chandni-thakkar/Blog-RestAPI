from django.urls import path
from .views import RegisterView, LoginView, TokenAccessView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/access/', TokenAccessView.as_view(), name='token_access'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
