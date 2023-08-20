from django.conf.urls import url
from ..views.admin import FollowUpRecordAPI

urlpatterns = [
    url(r"^follow_up_record/?$", FollowUpRecordAPI.as_view(), name="follow_up_record_api"),
]