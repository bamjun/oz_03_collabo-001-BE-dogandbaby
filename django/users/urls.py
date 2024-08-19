from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTTokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from django.urls import path

from .views.google_auth_view import GoogleExchangeCodeForToken, GoogleSocialLogout
from .views.kakao_auth_view import KakaoExchangeCodeForToken
from .views.mypage_views import (
    MyBookmarksView,
    MycommentView,
    MyProfileView,
    UpdateProfileImageView,
    UpdateProfileNameView,
    ViewHistoryView,
)
from .views.naver_auth_view import NaverExchangeCodeForToken

urlpatterns = [
    # google social
    path("google/login/callback/", GoogleExchangeCodeForToken.as_view(), name="google_callback"),  # 구글 로그인
    path("google/logout/", GoogleSocialLogout.as_view(), name="google-logout"),
    # naver social
    path("naver/login/callback/", NaverExchangeCodeForToken.as_view(), name="naver_callback"),  # 네이버 로그인
    # kakao social
    path("kakao/login/callback/", KakaoExchangeCodeForToken.as_view(), name="kakao_callback"),  # 카카오 로그인
    # 토큰 유효성 검사 엔드포인트
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    # 액세스 토큰 새로 발급해주는 엔드포인트
    path("api/token/refresh/", SimpleJWTTokenRefreshView.as_view(), name="token_refresh"),
    path("mypage/", MyProfileView.as_view(), name="mypage"),
    path("profile/", MyProfileView.as_view(), name="my-profile"),
    path("mypage/update-image/", UpdateProfileImageView.as_view(), name="mypage_update_profile_images"),
    path("mypage/update-name/", UpdateProfileNameView.as_view(), name="mypage_update_profile_names"),
    path("mypage/bookmark/", MyBookmarksView.as_view(), name="mypage_bookmark"),
    path("mypage/view-history/", ViewHistoryView.as_view(), name="mypage_view_history"),
    path("mypage/my-comment/", MycommentView.as_view(), name="mypage_my_comment"),
]
