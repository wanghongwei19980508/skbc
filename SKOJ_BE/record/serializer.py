from utils.api import serializers
from record.models import FollowUpRecord, OperationRecord, RollCallRecord
from account.serializers import UserSerializer

class CreateFollowUpRecordSerializer(serializers.Serializer):
    student = serializers.IntegerField()
    follow_up_stage = serializers.CharField(max_length=100)
    follow_up_content = serializers.CharField()
    actual_follow_up_time = serializers.DateTimeField()
    follow_up_method = serializers.CharField(max_length=100)
    # 下次跟进时间
    next_follow_up_time = serializers.DateTimeField(required=False, allow_null=True)
    # 下次跟进任务备注
    next_follow_up_task = serializers.CharField(max_length=100, required=False, allow_null=True)

class EditFollowUpRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    student = serializers.IntegerField()
    follow_up_stage = serializers.CharField(max_length=100)
    follow_up_content = serializers.CharField()
    actual_follow_up_time = serializers.DateTimeField()
    follow_up_method = serializers.CharField(max_length=100)
    # 下次跟进时间
    next_follow_up_time = serializers.DateTimeField(required=False, allow_null=True)
    # 下次跟进任务备注
    next_follow_up_task = serializers.CharField(max_length=100, required=False, allow_null=True)

class FollowUpRecordSerializer(serializers.ModelSerializer):
    follow_up_person = UserSerializer()
    class Meta:
        model = FollowUpRecord
        fields = "__all__"