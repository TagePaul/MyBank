from django.contrib import admin
from django.urls import path, re_path, include
from .router import router
# from user.urls import router
from rest_framework_simplejwt import views as jwt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    re_path(r"^api/jwt/create/?", 
        jwt.TokenObtainPairView.as_view(), 
        name="jwt-create"),
    re_path(r"^api/jwt/refresh/?", 
        jwt.TokenRefreshView.as_view(), 
        name="jwt-refresh"),
    re_path(r"^api/jwt/verify/?", 
        jwt.TokenVerifyView.as_view(), 
        name="jwt-verify"),
]

