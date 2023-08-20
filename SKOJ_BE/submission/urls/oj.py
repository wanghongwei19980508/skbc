from django.conf.urls import url

from ..views.oj import SubmissionAPI, SubmissionListAPI, ContestSubmissionListAPI, SubmissionExistsAPI, \
                        ObjectiveSubmissionAPI, ObjectiveSubmissionExistsAPI, ObjectiveSubmissionListAPI, ContestObjectiveSubmissionListAPI

urlpatterns = [
    url(r"^submission/?$", SubmissionAPI.as_view(), name="submission_api"),
    url(r"^submissions/?$", SubmissionListAPI.as_view(), name="submission_list_api"),
    url(r"^submission_exists/?$", SubmissionExistsAPI.as_view(), name="submission_exists"),
    url(r"^contest_submissions/?$", ContestSubmissionListAPI.as_view(), name="contest_submission_list_api"),
    url(r"^objective_submission/?$", ObjectiveSubmissionAPI.as_view(), name="objective_submission_api"),
    url(r"^objective_submissions/?$", ObjectiveSubmissionListAPI.as_view(), name="objective_submission_list_api"),
    url(r"^objective_submission_exists/?$", ObjectiveSubmissionExistsAPI.as_view(), name="objective_submission_exists"),
    url(r"^contest_objective_submissions/?$", ContestObjectiveSubmissionListAPI.as_view(), name="contest_objective_submission_list_api"),
]
