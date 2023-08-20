from django.conf.urls import url

from ..views import JudgeServerHeartbeatAPI, LanguagesAPI, WebsiteConfigAPI, SoftwaresAPI, SlideshowsAPI

urlpatterns = [
    url(r"^website/?$", WebsiteConfigAPI.as_view(), name="website_info_api"),
    url(r"^softwares/?$", SoftwaresAPI.as_view(), name="softwares_api"),
    url(r"^slideshows/?$", SlideshowsAPI.as_view(), name="slideshows_api"),
    url(r"^judge_server_heartbeat/?$", JudgeServerHeartbeatAPI.as_view(), name="judge_server_heartbeat_api"),
    url(r"^languages/?$", LanguagesAPI.as_view(), name="language_list_api")
]
