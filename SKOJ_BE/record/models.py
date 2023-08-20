from django.db import models
from utils.models import JSONField
from account.models import User, Clue
from course.models import Course, Lesson

'''
跟进记录:
    1. 创建时间
    2. 跟进人
    3. 计划跟进时间
    4. 学员
    5. 跟进阶段
    6. 跟进内容
    7. 实际跟进时间
    8. 跟进方式
    9. 照片
'''


class FollowUpRecord(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    follow_up_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    plan_follow_up_time = models.DateTimeField(null=True)
    student = models.ForeignKey(Clue, on_delete=models.SET_NULL, null=True)
    follow_up_stage = models.TextField(null=True)
    follow_up_content = models.TextField(null=True)
    actual_follow_up_time = models.DateTimeField(null=True)
    follow_up_method = models.TextField(null=True)

    class Meta:
        db_table = "follow_up_record"
        ordering = ("create_time",)


'''
操作记录:
    1. 操作时间
    2. 操作内容
    3. 操作类型
    4. 操作人员
    5. 操作人账号
'''


class OperationRecord(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    operation_content = models.TextField()
    operation_type = models.TextField()
    operation_person = models.ForeignKey(User, on_delete=models.CASCADE)
    operation_person_account = models.TextField()

    class Meta:
        db_table = "operation_record"
        ordering = ("create_time",)


'''
点名记录:
    1. 点名时间
    2. 对应班级
    3. 对应课次
    4. 上课老师
    5. 到课状态
    6. 学员
    7. 消耗方式
    8. 扣除额度
    9. 课消金额
'''


class RollCallRecord(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    grade = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rollcall_teacher")
    attendance_status = models.TextField()
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rollcall_student")
    consumption_method = models.TextField()
    deduct_quota = models.IntegerField()
    consumption_amount = models.IntegerField()

    class Meta:
        db_table = "roll_call_record"
        ordering = ("create_time",)


'''
点评记录:
    1. 点评时间
    2. 对应班级
    3. 对应课次
    4. 上课老师
    5. 学员
    6. 点评内容
    7. 点评分数
'''

class CommentRecord(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    grade = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_teacher")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_student")
    comment_content = models.TextField()
    comment_score = JSONField()

    class Meta:
        db_table = "comment_record"
        ordering = ("create_time",)

'''
批量操作记录
    操作时间
    操作类型
    操作状态
    成功数量
    失败数量
    操作人员
    操作内容-JSON->便于导出
    操作备注
'''
class BatchOperationRecord(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    operation_type = models.TextField()
    operation_status = models.TextField()
    success_amount = models.IntegerField()
    failure_amount = models.IntegerField()
    operation_person = models.ForeignKey(User, on_delete=models.CASCADE)
    operation_content = JSONField()
    operation_remark = models.TextField()
    
    class Meta:
        db_table = "batch_operation_record"
        ordering = ("create_time",)


'''
订单记录:
    1. 订单号
    2. 创建时间
    3. 订单类型
    4. 订单状态
    5. 订单来源
    6. 订单金额
    7. 对应学员
    8. 购买内容
    9. 支付记录
'''