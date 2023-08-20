import random
from django.db.models import Q, Count
from account.models import AdminType
from utils.api import APIView
from account.decorators import check_contest_permission
from ..models import ProblemTag, Problem, ProblemRuleType, ObjectiveProblem, ObjectiveProblemTag
from ..serializers import ProblemAdminSerializer, ProblemSerializer, TagSerializer, ProblemSafeSerializer, ObjectiveProblemSerializer, ObjectiveProblemSafeSerializer, ObjectiveTagSerializer
from contest.models import ContestRuleType
from judge.dispatcher import ChooseJudgeServer, logger
from urllib.parse import urljoin
from options.options import SysOptions
import hashlib
import requests


class SelfTest(APIView):
    def __init__(self):
        self.token = hashlib.sha256(SysOptions.judge_server_token.encode("utf-8")).hexdigest()

    def _request(self, url, data=None):
        kwargs = {"headers": {"X-Judge-Server-Token": self.token}}
        if data:
            kwargs["json"] = data
        try:
            return requests.post(url, **kwargs).json()
        except Exception as e:
            logger.exception(e)

    def get(self, request):
        if not request.user.is_authenticated:
            return self.error("Not logged in")
        if not request.GET.get("src"):
            return self.error("No source code")
        if not request.GET.get("lang"):
            return self.error("No language")
        if not request.GET.get("input"):
            return self.error("No input")
        if not request.GET.get("output"):
            return self.error("No output")
        language = request.GET.get("lang")
        data = {
            "language_config": list(filter(lambda item: language == item["name"], SysOptions.languages))[0]["config"],
            "src": request.GET.get("src"),
            "max_cpu_time": request.GET.get("max_cpu_time") or 1000,
            "max_memory": request.GET.get("max_memory") or 128 * 1024 * 1024,
            "test_case": {
                "input": request.GET.get("input"),
                "output": request.GET.get("output")
            },
            "output": True,
        }
        with ChooseJudgeServer() as server:
            if not server:
                return self.error("No judge server available")
            resp = self._request(urljoin(server.service_url, "/self_test"), data=data)
        if not resp:
            return self.error("No judge server available")
        if resp["err"]:
            return self.error(msg=resp["err"], err=resp["data"])
        return self.success(resp["data"])


class ProblemTagAPI(APIView):
    def get(self, request):
        qs = ProblemTag.objects
        keyword = request.GET.get("keyword")
        if keyword:
            qs = ProblemTag.objects.filter(name__icontains=keyword)
        tags = qs.annotate(problem_count=Count("problem")).filter(problem_count__gt=0)
        return self.success(TagSerializer(tags, many=True).data)

class ObjectiveProblemTagAPI(APIView):
    def get(self, request):
        qs = ObjectiveProblemTag.objects
        keyword = request.GET.get("keyword")
        if keyword:
            qs = ObjectiveProblemTag.objects.filter(name__icontains=keyword)
        tags = qs.annotate(objective_problem_count=Count("objectiveproblem")).filter(objective_problem_count__gt=0)
        return self.success(ObjectiveTagSerializer(tags, many=True).data)

class PickOneObjectiveAPI(APIView):
    def get(self, request):
        objective_problems = ObjectiveProblem.objects.filter(visible=True)
        count = objective_problems.count()
        if count == 0:
            return self.error("No objective problem to pick")
        return self.success(objective_problems[random.randint(0, count - 1)]._id)

class PickOneAPI(APIView):
    def get(self, request):
        problems = Problem.objects.filter(contest_id__isnull=True, visible=True)
        count = problems.count()
        if count == 0:
            return self.error("No problem to pick")
        return self.success(problems[random.randint(0, count - 1)]._id)

class ObjectiveProblemAPI(APIView):   
    def get(self, request):
        # 问题详情页
        objective_problem_id = request.GET.get("objective_problem_id")
        if objective_problem_id:
            try:
                problem = ObjectiveProblem.objects.select_related("created_by") \
                    .get(_id=objective_problem_id, contest_id__isnull=True, visible=True)
                problem_data = ObjectiveProblemSerializer(problem).data
                # self._add_problem_status(request, problem_data)
                return self.success(problem_data)
            except ObjectiveProblem.DoesNotExist:
                return self.error("Objective Problem does not exist")
        objective_problem_by_id = request.GET.get("objective_problem_by_id")
        if objective_problem_by_id:
            try:
                problem = ObjectiveProblem.objects.select_related("created_by") \
                    .get(id=objective_problem_by_id, contest_id__isnull=True, visible=True)
                problem_data = ObjectiveProblemSerializer(problem).data
                # self._add_problem_status(request, problem_data)
                return self.success(problem_data)
            except ObjectiveProblem.DoesNotExist:
                return self.error("Objective Problem does not exist")
        limit = request.GET.get("limit")
        if not limit:
            return self.error("Limit is needed")

        problems = ObjectiveProblem.objects.select_related("created_by").filter(contest_id__isnull=True, visible=True)
        # 按照标签筛选
        tag_text = request.GET.get("tag")
        if tag_text:
            problems = problems.filter(tags__name=tag_text)

        # 搜索的情况
        keyword = request.GET.get("keyword", "").strip()
        if keyword:
            problems = problems.filter(Q(title__icontains=keyword) | Q(_id__icontains=keyword))

        # 难度筛选
        difficulty = request.GET.get("difficulty")
        if difficulty:
            problems = problems.filter(difficulty=difficulty)
        # 类型筛选
        type = request.GET.get("type")
        if type:
            problems = problems.filter(type=type)
        # 根据profile 为做过的题目添加标记
        data = self.paginate_data(request, problems, ObjectiveProblemSerializer)
        # self._add_problem_status(request, data)
        return self.success(data)

class ProblemAPI(APIView):
    @staticmethod
    def _add_problem_status(request, queryset_values):
        if request.user.is_authenticated:
            profile = request.user.userprofile
            acm_problems_status = profile.acm_problems_status.get("problems", {})
            oi_problems_status = profile.oi_problems_status.get("problems", {})
            # paginate data
            results = queryset_values.get("results")
            if results is not None:
                problems = results
            else:
                problems = [queryset_values, ]
            for problem in problems:
                if problem["rule_type"] == ProblemRuleType.ACM:
                    problem["my_status"] = acm_problems_status.get(str(problem["id"]), {}).get("status")
                else:
                    problem["my_status"] = oi_problems_status.get(str(problem["id"]), {}).get("status")

    def get(self, request):
        # 问题详情页
        problem_id = request.GET.get("problem_id")
        if problem_id:
            try:
                problem = Problem.objects.select_related("created_by") \
                    .get(_id=problem_id, contest_id__isnull=True, visible=True)
                if request.user.admin_type in [AdminType.STUDENT, AdminType.REGULAR_USER]:
                    problem_data = ProblemSerializer(problem).data
                else:
                    problem_data = ProblemAdminSerializer(problem).data
                self._add_problem_status(request, problem_data)
                return self.success(problem_data)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist")

        limit = request.GET.get("limit")
        if not limit:
            return self.error("Limit is needed")

        problems = Problem.objects.select_related("created_by").filter(contest_id__isnull=True, visible=True)
        # 按照标签筛选
        tag_text = request.GET.get("tag")
        if tag_text:
            problems = problems.filter(tags__name=tag_text)

        # 搜索的情况
        keyword = request.GET.get("keyword", "").strip()
        if keyword:
            problems = problems.filter(Q(title__icontains=keyword) | Q(_id__icontains=keyword))

        # 难度筛选
        difficulty = request.GET.get("difficulty")
        if difficulty:
            problems = problems.filter(difficulty=difficulty)
        # 根据profile 为做过的题目添加标记
        data = self.paginate_data(request, problems, ProblemSerializer)
        self._add_problem_status(request, data)
        return self.success(data)

class ContestProblemAPI(APIView):
    def _add_problem_status(self, request, queryset_values):
        if request.user.is_authenticated:
            profile = request.user.userprofile
            if self.contest.rule_type == ContestRuleType.ACM:
                problems_status = profile.acm_problems_status.get("contest_problems", {})
            else:
                problems_status = profile.oi_problems_status.get("contest_problems", {})
            for problem in queryset_values:
                problem["my_status"] = problems_status.get(str(problem["id"]), {}).get("status")

    @check_contest_permission(check_type="problems")
    def get(self, request):
        problem_id = request.GET.get("problem_id")
        if problem_id:
            try:
                problem = Problem.objects.select_related("created_by").get(_id=problem_id,
                                                                           contest=self.contest,
                                                                           visible=True)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist.")
            if self.contest.problem_details_permission(request.user):
                problem_data = ProblemSerializer(problem).data
                self._add_problem_status(request, [problem_data, ])
            else:
                problem_data = ProblemSafeSerializer(problem).data
            return self.success(problem_data)

        contest_problems = Problem.objects.select_related("created_by").filter(contest=self.contest, visible=True)
        if self.contest.problem_details_permission(request.user):
            data = ProblemSerializer(contest_problems, many=True).data
            self._add_problem_status(request, data)
        else:
            data = ProblemSafeSerializer(contest_problems, many=True).data
        return self.success(data)

class ContestObjectiveProblemAPI(APIView):
    def _add_problem_status(self, request, queryset_values):
        if request.user.is_authenticated:
            profile = request.user.userprofile
            if self.contest.rule_type == ContestRuleType.ACM:
                problems_status = profile.acm_problems_status.get("contest_objective_problems", {})
            else:
                problems_status = profile.oi_problems_status.get("contest_objective_problems", {})
            for problem in queryset_values:
                problem["my_status"] = problems_status.get(str(problem["id"]), {}).get("status")

    @check_contest_permission(check_type="problems")
    def get(self, request):
        objective_problem_id = request.GET.get("objective_problem_id")
        if objective_problem_id:
            try:
                objective_problem = ObjectiveProblem.objects.select_related("created_by").get(_id=objective_problem_id,
                                                                           contest=self.contest,
                                                                           visible=True)
            except ObjectiveProblem.DoesNotExist:
                return self.error("Objective Problem does not exist.")
            if self.contest.problem_details_permission(request.user):
                objective_problem_data = ObjectiveProblemSerializer(objective_problem).data
                self._add_problem_status(request, [objective_problem_data, ])
            else:
                objective_problem_data = ObjectiveProblemSafeSerializer(objective_problem).data
            return self.success(objective_problem_data)

        contest_objective_problems = ObjectiveProblem.objects.select_related("created_by").filter(contest=self.contest, visible=True)
        if self.contest.problem_details_permission(request.user):
            data = ObjectiveProblemSerializer(contest_objective_problems, many=True).data
            self._add_problem_status(request, data)
        else:
            data = ObjectiveProblemSafeSerializer(contest_objective_problems, many=True).data
        return self.success(data)