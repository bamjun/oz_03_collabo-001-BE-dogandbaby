from common.models import CommonModel
from users.utils import generate_random_nickname

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    # 이 로그인시 수정필요한데 월요일에 수정하고 주석 삭제할게요 -주영광-
    nickname = models.CharField(max_length=255, unique=True, verbose_name="닉네임", default=generate_random_nickname())
    profile_image = models.ImageField(upload_to="users/profile_image/", blank=True, null=True)
    is_staff = models.BooleanField(default=False, verbose_name="운영진")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="가입일자")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일자")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class BookMark(CommonModel):
    from places.models import Place

    id = models.BigAutoField(primary_key=True)  # Primary Key, Unique Identifier
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookmarks")  # Foreign Key로 User 참조
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="bookmarks")  # Foreign Key로 Place 참조
    bookmark_check = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.nickname} - {self.place.name}"


class ViewHistory(CommonModel):
    from places.models import Place

    id = models.BigAutoField(primary_key=True)  # Primary Key, Unique Identifier
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="view_histories"
    )  # Foreign Key로 User 참조
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name="view_histories"
    )  # Foreign Key로 Place 참조
    bookmark = models.ForeignKey(
        BookMark, on_delete=models.CASCADE, related_name="view_histories"
    )  # Foreign Key로 Bookmark 참조

    def __str__(self):
        return f"{self.user.nickname} - {self.place.name}"
