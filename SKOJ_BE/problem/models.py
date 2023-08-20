from django.db import models
from utils.models import JSONField

from account.models import User
from contest.models import Contest
from utils.models import RichTextField
from utils.constants import Choices


class ProblemTag(models.Model):
    name = models.TextField()

    class Meta:
        db_table = "problem_tag"


class ObjectiveProblemTag(models.Model):
    name = models.TextField()

    class Meta:
        db_table = "objective_problem_tag"


class ProblemRuleType(Choices):
    ACM = "ACM"
    OI = "OI"


class ProblemDifficulty(object):
    High = "High"
    Mid = "Mid"
    Low = "Low"


class ProblemIOMode(Choices):
    standard = "Standard IO"
    file = "File IO"


def _default_io_mode():
    return {"io_mode": ProblemIOMode.standard, "input": "input.txt", "output": "output.txt"}


class Problem(models.Model):
    # display ID
    _id = models.TextField(db_index=True)
    contest = models.ForeignKey(Contest, null=True, on_delete=models.CASCADE)
    # lesson = models.ForeignKey(Lesson, null=True, on_delete=models.CASCADE)
    # for contest problem
    is_public = models.BooleanField(default=False)
    title = models.TextField()
    # HTML
    description = RichTextField()
    input_description = RichTextField()
    output_description = RichTextField()
    # [{input: "test", output: "123"}, {input: "test123", output: "456"}]
    samples = JSONField()
    test_case_id = models.TextField()
    # [{"input_name": "1.in", "output_name": "1.out", "score": 0}]
    test_case_score = JSONField()
    hint = RichTextField(null=True)
    languages = JSONField()
    template = JSONField()
    std_code = JSONField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    # we can not use auto_now here
    last_update_time = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # ms
    time_limit = models.IntegerField()
    # MB
    memory_limit = models.IntegerField()
    # io mode
    io_mode = JSONField(default=_default_io_mode)
    # special judge related
    spj = models.BooleanField(default=False)
    spj_language = models.TextField(null=True)
    spj_code = models.TextField(null=True)
    spj_version = models.TextField(null=True)
    spj_compile_ok = models.BooleanField(default=False)
    rule_type = models.TextField()
    visible = models.BooleanField(default=True)
    difficulty = models.TextField()
    tags = models.ManyToManyField(ProblemTag)
    source = models.TextField(null=True)
    # for OI mode
    total_score = models.IntegerField(default=0)
    submission_number = models.BigIntegerField(default=0)
    accepted_number = models.BigIntegerField(default=0)
    # {JudgeStatus.ACCEPTED: 3, JudgeStaus.WRONG_ANSWER: 11}, the number means count
    statistic_info = JSONField(default=dict)
    share_submission = models.BooleanField(default=False)

    class Meta:
        db_table = "problem"
        unique_together = (("_id", "contest"),)
        ordering = ("create_time",)

    def add_submission_number(self):
        self.submission_number = models.F("submission_number") + 1
        self.save(update_fields=["submission_number"])

    def add_ac_number(self):
        self.accepted_number = models.F("accepted_number") + 1
        self.save(update_fields=["accepted_number"])


class ObjectiveProblem(models.Model):
    # display ID
    _id = models.TextField(db_index=True)
    is_public = models.BooleanField(default=False)
    contest = models.ForeignKey(Contest, null=True, on_delete=models.CASCADE)
    # lesson = models.ForeignKey(Lesson, null=True, on_delete=models.CASCADE)
    title = models.TextField()
    type = models.TextField()
    # HTML
    description = RichTextField()
    options = JSONField()
    answer = JSONField()
    hint = RichTextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
    difficulty = models.TextField()
    source = models.TextField(null=True)
    tags = models.ManyToManyField(ObjectiveProblemTag)
    total_score = models.IntegerField(default=0)
    submission_number = models.BigIntegerField(default=0)
    accepted_number = models.BigIntegerField(default=0)

    is_multiple = models.BooleanField(default=False, null=True)
    multiple_answer = JSONField(null=True)
    '''
    multiple_answer = [
        {
            "id":1,
            "answer":[
                {
                "isAns": true,
                "option": ""
                },
                {
                    "isAns": false,
                    "option": ""
                },
                {
                    "isAns": false,
                    "option": ""
                },
                {
                    "isAns": false,
                    "option": ""
                }
            ]
        },
        {
            "id":2,
            "answer":[
                {
                "isAns": true,
                "option": ""
                },
                {
                    "isAns": false,
                    "option": ""
                },
                {
                    "isAns": false,
                    "option": ""
                },
                {
                    "isAns": false,
                    "option": ""
                }
            ]
        },
        {
            "id":3,
            "answer":[
                {
                "isAns": true,
                "option": ""
                },
                {
                    "isAns": false,
                    "option": ""
                }
            ]
        }
    ]
    '''
    multiple_problem = JSONField(null=True)
    '''
    multiple_problem:[
        {   "id" : 1
            "type": "single",
            "options": ["123", "2", "3", "4"],
            "description": "1+1=?",
            "score":2,
        },
        {   "id" : 2
            "type": "multiple",
            "options": ["123", "2", "3", "4"],
            "description": "1+2<?",
            "score":2,
        },
        {   "id" : 3
            "type": "true_flase",
            "options": ['正确', '错误'],
            "description": "1+1=2",
            "score":2,
        },
    ]
    '''

    class Meta:
        db_table = "objective_problem"
        unique_together = (("_id", "contest"),)
        ordering = ("create_time",)

    def add_submission_number(self):
        self.submission_number = models.F("submission_number") + 1
        self.save(update_fields=["submission_number"])

    def add_ac_number(self):
        self.accepted_number = models.F("accepted_number") + 1
        self.save(update_fields=["accepted_number"])
