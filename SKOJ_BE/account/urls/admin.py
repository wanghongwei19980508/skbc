from django.conf.urls import url

from ..views.admin import UserAdminAPI, GenerateUserAPI, PicUploadAPI, ClueAPI

urlpatterns = [
    url(r"^user/?$", UserAdminAPI.as_view(), name="user_admin_api"),
    url(r"^generate_user/?$", GenerateUserAPI.as_view(), name="generate_user_api"),
    url(r"^pic_upload/?$", PicUploadAPI.as_view(), name="pic_upload"),
    url(r"^clue/?$", ClueAPI.as_view(), name="clue_api"),
]
