from account.decorators import super_admin_required
from judge.tasks import judge_task
# from judge.dispatcher import JudgeDispatcher
from utils.api import APIView
from ..models import Submission, ObjectiveSubmission, ObjectiveStatus, ObjectiveProblem


class SubmissionRejudgeAPI(APIView):
    @super_admin_required
    def get(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Parameter error, id is required")
        try:
            submission = Submission.objects.select_related("problem").get(id=id, contest_id__isnull=True)
        except Submission.DoesNotExist:
            return self.error("Submission does not exists")
        submission.statistic_info = {}
        submission.save()

        judge_task.send(submission.id, submission.problem.id)
        return self.success()

class ObjectiveSubmissionRejudgeAPI(APIView):
    @super_admin_required
    def get(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Parameter error, id is required")
        try:
            submission = ObjectiveSubmission.objects.select_related("objective_problem").get(id=id, contest_id__isnull=True)
        except ObjectiveSubmission.DoesNotExist:
            return self.error("Submission does not exists")
        try:
            problem = ObjectiveProblem.objects.get(id=submission.objective_problem_id, visible=True)
        except ObjectiveProblem.DoesNotExist:
            return self.error("Objective Problem not exist")
        result = ObjectiveStatus.CORRECT
        for i, option in enumerate(problem.answer):
            if option['isAns']:
                if i not in submission.choice:
                    result = ObjectiveStatus.WRONG
                    break
            elif i in submission.choice:
                result = ObjectiveStatus.WRONG
                break
        if not submission.result == result:
            if result:
                problem.accepted_number += 2
            else:
                problem.accepted_number -= 2
            submission.result = result
            problem.save(update_fields=["accepted_number",])
        submission.save()
        return self.success()