from django.conf.urls import url

from ..views.admin import SubmissionRejudgeAPI, ObjectiveSubmissionRejudgeAPI

urlpatterns = [
    url(r"^submission/rejudge?$", SubmissionRejudgeAPI.as_view(), name="submission_rejudge_api"),
    url(r"^objective_submission/rejudge?$", ObjectiveSubmissionRejudgeAPI.as_view(), name="objective_submission_rejudge_api"),
]
