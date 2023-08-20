from django.conf.urls import url

from ..views.oj import ProblemTagAPI, ProblemAPI, ContestObjectiveProblemAPI, ContestProblemAPI, PickOneAPI, PickOneObjectiveAPI, ObjectiveProblemAPI, ObjectiveProblemTagAPI, SelfTest

urlpatterns = [
    url(r"^problem/tags/?$", ProblemTagAPI.as_view(), name="problem_tag_list_api"),
    url(r"^objective_problem/tags/?$", ObjectiveProblemTagAPI.as_view(), name="objective_problem_tag_list_api"),
    url(r"^problem/?$", ProblemAPI.as_view(), name="problem_api"),
    url(r"^objective_problem/?$", ObjectiveProblemAPI.as_view(), name="objective_problem_api"),
    url(r"^pickone/?$", PickOneAPI.as_view(), name="pick_one_api"),
    url(r"^pickone_objective/?$", PickOneObjectiveAPI.as_view(), name="pick_one_objective_api"),
    url(r"^contest/problem/?$", ContestProblemAPI.as_view(), name="contest_problem_api"),
    url(r"^contest/objective_problem/?$", ContestObjectiveProblemAPI.as_view(), name="contest_objective_problem_api"),
    url(r"^self_test/?$", SelfTest.as_view(), name="self_test"),
]
