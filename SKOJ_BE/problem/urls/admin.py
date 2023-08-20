from django.conf.urls import url

from ..views.admin import (ContestProblemAPI, ProblemAPI, TestCaseAPI, MakeContestProblemPublicAPIView, AddContestObjectiveProblemAPI,
                           CompileSPJAPI, AddContestProblemAPI, ExportProblemAPI, ImportProblemAPI, ExportObjectiveProblemAPI, 
                           ObjectiveProblemAPI, ContestObjectiveProblemAPI, FPSProblemImport, MakeContestObjectiveProblemPublicAPIView,)
                        #    LessonProblemAPI, LessonObjectiveProblemAPI, MakeLessonProblemPublicAPIView, MakeLessonObjectiveProblemPublicAPIView,
                        #    AddLessonProblemAPI, AddLessonObjectiveProblemAPI)

urlpatterns = [
    url(r"^test_case/?$", TestCaseAPI.as_view(), name="test_case_api"),
    url(r"^compile_spj/?$", CompileSPJAPI.as_view(), name="compile_spj"),
    url(r"^problem/?$", ProblemAPI.as_view(), name="problem_admin_api"),
    url(r"^objective_problem/?$", ObjectiveProblemAPI.as_view(), name="objective_problem_admin_api"),
    url(r"^contest/problem/?$", ContestProblemAPI.as_view(), name="contest_problem_admin_api"),
    url(r"^contest/objective_problem/?$", ContestObjectiveProblemAPI.as_view(), name="contest_objective_problem_admin_api"),
    url(r"^contest_problem/make_public/?$", MakeContestProblemPublicAPIView.as_view(), name="make_public_api"),
    url(r"^contest_objective_problem/make_public/?$", MakeContestObjectiveProblemPublicAPIView.as_view(), name="make_objective_public_api"),
    url(r"^contest/add_problem_from_public/?$", AddContestProblemAPI.as_view(), name="add_contest_problem_from_public_api"),
    url(r"^contest/add_objective_problem_from_public/?$", AddContestObjectiveProblemAPI.as_view(), name="add_contest_objective_problem_from_public_api"),
    # url(r"^lesson/problem/?$", LessonProblemAPI.as_view(), name="lesson_problem_admin_api"),
    # url(r"^lesson/objective_problem/?$", LessonObjectiveProblemAPI.as_view(), name="lesson_objective_problem_admin_api"),
    # url(r"^lesson_problem/make_public/?$", MakeLessonProblemPublicAPIView.as_view(), name="make_lesson_problem_public_api"),
    # url(r"^lesson_objective_problem/make_public/?$", MakeLessonObjectiveProblemPublicAPIView.as_view(), name="make_lesson_objective_public_api"),
    # url(r"^lesson/add_problem_from_public/?$", AddLessonProblemAPI.as_view(), name="add_lesson_problem_from_public_api"),
    # url(r"^lesson/add_objective_problem_from_public/?$", AddLessonObjectiveProblemAPI.as_view(), name="add_lesson_objective_problem_from_public_api"),
    url(r"^export_problem/?$", ExportProblemAPI.as_view(), name="export_problem_api"),
    url(r"^export_objective_problem/?$", ExportObjectiveProblemAPI.as_view(), name="export_objective_problem_api"),
    url(r"^import_problem/?$", ImportProblemAPI.as_view(), name="import_problem_api"),
    url(r"^import_fps/?$", FPSProblemImport.as_view(), name="fps_problem_api"),
]
