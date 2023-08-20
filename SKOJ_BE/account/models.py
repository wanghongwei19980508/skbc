from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.db import models
from utils.models import JSONField
from phonenumber_field.modelfields import PhoneNumberField

'''
用户类型/角色分类:学员，讲师，学管，管理员，超级管理员
'''
class AdminType(object):
    REGULAR_USER = "Regular User" # 普通用户 -  无管理权限 自我注册
    STUDENT = 'Student' # 学员 - 无管理权限
    LECTURER = 'Lecturer' # 讲师 - 有部分管理权限
    SCHOOL_MANAGER = 'School Manager' # 学管 - 有自己所管部分的全部权限+用户导入权限
    TEACHER_RESEARCHER = 'Teacher Researcher' # 教研 - 有自己所管部分的全部权限+用户导入权限
    ADMIN = "Admin" # 普通管理员 - 有大部分权限，可多人 
    SUPER_ADMIN = "Super Admin" # 超级管理员 - 有所有权限 仅一个账号

'''
权限等级
'''
class Permission(object):
    NONE = "None"
    OWN = "Own"
    ALL = "All"

class UserManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        return self.get(**{f"{self.model.USERNAME_FIELD}__iexact": username})


class StudentStatus(object):
    # 潜在学员
    POTENTIAL_STUDENT = "潜在学员"
    # 在读学员
    STUDENT = "在读学员"
    # 历史学员
    HISTORY_STUDENT = "历史学员"

class FollowStatus(object):
    # 跟进中
    FOLLOWING = "跟进中"
    # 待跟进
    TO_BE_FOLLOWED = "待跟进"
    # 未分配
    UNALLOCATED = "未分配"
    # 已成交
    DEAL = "已成交"

class User(AbstractBaseUser):
    username = models.TextField(unique=True)
    email = models.TextField(null=True)
    phone = PhoneNumberField(null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    # One of UserType
    admin_type = models.TextField(default=AdminType.REGULAR_USER)
    problem_permission = models.TextField(default=Permission.NONE)
    course_permission = models.TextField(default=Permission.NONE)
    reset_password_token = models.TextField(null=True)
    reset_password_token_expire_time = models.DateTimeField(null=True)
    # SSO auth token
    auth_token = models.TextField(null=True)
    two_factor_auth = models.BooleanField(default=False)
    tfa_token = models.TextField(null=True)
    session_keys = JSONField(default=list)
    # open api key
    open_api = models.BooleanField(default=False)
    open_api_appkey = models.TextField(null=True)
    is_disabled = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def is_student_role(self):
        return self.admin_type in [AdminType.ADMIN, AdminType.SUPER_ADMIN, AdminType.STUDENT]

    def is_lecturer_role(self):
        return self.admin_type in [AdminType.ADMIN, AdminType.SUPER_ADMIN, AdminType.LECTURER]
    
    def is_school_manager_role(self):
        return self.admin_type in [AdminType.ADMIN, AdminType.SUPER_ADMIN, AdminType.SCHOOL_MANAGER]
    
    def is_teacher_researcher_role(self):
        return self.admin_type in [AdminType.ADMIN, AdminType.SUPER_ADMIN, AdminType.TEACHER_RESEARCHER]

    # 如果仅仅是管理员的话 只筛选自己本身创建的
    def is_admin(self):
        return self.admin_type == AdminType.ADMIN

    def is_super_admin(self):
        return self.admin_type == AdminType.SUPER_ADMIN

    def is_admin_role(self):
        return self.admin_type in [AdminType.ADMIN, AdminType.SUPER_ADMIN]

    def can_mgmt_all_problem(self):
        return self.problem_permission == Permission.ALL

    def can_mgmt_all_course(self):
        return self.course_permission == Permission.ALL

    def is_contest_admin(self, contest):
        return self.is_authenticated and (contest.created_by == self or self.admin_type == AdminType.SUPER_ADMIN)

    def is_course_admin(self, course):
        return self.is_authenticated and (course.created_by == self or self.course_permission == Permission.ALL)
    
    class Meta:
        db_table = "user"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # acm_problems_status examples:
    # {
    #     "problems": {
    #         "1": {
    #             "status": JudgeStatus.ACCEPTED,
    #             "_id": "1000"
    #         }
    #     },
    #     "contest_problems": {
    #         "1": {
    #             "status": JudgeStatus.ACCEPTED,
    #             "_id": "1000"
    #         }
    #     }
    # }
    acm_problems_status = JSONField(default=dict)
    # like acm_problems_status, merely add "score" field
    oi_problems_status = JSONField(default=dict)

    real_name = models.TextField(null=True)
    avatar = models.TextField(default=f"{settings.AVATAR_URI_PREFIX}/default.png")
    blog = models.URLField(null=True)
    mood = models.TextField(null=True)
    github = models.TextField(null=True)
    school = models.TextField(null=True)
    major = models.TextField(null=True)
    language = models.TextField(null=True)
    # for ACM
    accepted_number = models.IntegerField(default=0)
    # for OI
    total_score = models.BigIntegerField(default=0)
    submission_number = models.IntegerField(default=0)

    def add_accepted_problem_number(self):
        self.accepted_number = models.F("accepted_number") + 1
        self.save()

    def add_submission_number(self):
        self.submission_number = models.F("submission_number") + 1
        self.save()

    # 计算总分时， 应先减掉上次该题所得分数， 然后再加上本次所得分数
    def add_score(self, this_time_score, last_time_score=None):
        last_time_score = last_time_score or 0
        self.total_score = models.F("total_score") - last_time_score + this_time_score
        self.save()

    class Meta:
        db_table = "user_profile"

'''
线索表
    学生姓名
    手机号主
    手机号
    性别
    年龄
    就读学校
    当前年级
    备用号主
    备用号码
    家庭住址
    意向级别
    跟进人-外键用户
    标签
    备注
    外键用户
    线索头像
    跟进状态
    跟进阶段
'''
class Clue(models.Model):
    student_name = models.TextField(null=True)
    phone = PhoneNumberField(null=True)
    # 号主
    phone_owner = models.TextField(null=True)
    # 性别
    gender = models.TextField(null=True)
    # 年龄
    age = models.TextField(null=True)
    # 就读学校
    school = models.TextField(null=True)
    # 当前年级
    grade = models.TextField(null=True)
    # 备用号主
    spare_phone_owner = models.TextField(null=True)
    # 备用号码
    spare_phone = PhoneNumberField(null=True)
    # 家庭住址
    address = models.TextField(null=True)
    # 意向级别
    intention_level = models.TextField(null=True)
    # 跟进人
    follow_up = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='follow_up')
    # 备注
    remark = models.TextField(null=True)
    # 对应oj账号-用户外键
    oj_account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='oj_account')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)
    # 线索头像
    avatar = models.TextField(default=f"{settings.AVATAR_URI_PREFIX}/default.png")
    # 跟进状态
    follow_status = models.TextField(null=True)
    # 跟进阶段
    follow_stage = models.TextField(null=True)
    # 学员状态
    student_status = models.TextField(default=StudentStatus.POTENTIAL_STUDENT, null=True)
    # 小鹅通手机号
    xiaoe_phone = PhoneNumberField(null=True)

    class Meta:
        db_table = "clue"
